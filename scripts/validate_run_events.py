#!/usr/bin/env python3
"""Validate cybernetic run-event JSON/JSONL files.

The validator intentionally uses only the Python standard library. It enforces
the repository's metadata-only safety contract rather than attempting full JSON
Schema coverage.
"""

from __future__ import annotations

import argparse
import json
import re
import socket
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


EVENT_TYPES = {
    "skill_invoked",
    "route_decided",
    "artifact_created",
    "blocked",
    "human_feedback",
    "runtime_outcome",
}

REQUIRED_FIELDS = {
    "schema_version",
    "event_id",
    "event",
    "timestamp",
    "privacy_mode",
    "machine_id",
    "skill_pack",
    "status",
    "task_hash",
}

UNSAFE_METADATA_ONLY_KEYS = {
    "artifact_body",
    "code",
    "code_excerpt",
    "content_excerpt",
    "content_summary",
    "credential",
    "credentials",
    "customer_data",
    "log",
    "log_excerpt",
    "path",
    "prompt",
    "raw_prompt",
    "raw_response",
    "real_path",
    "real_repo",
    "repo_name",
    "repository",
    "repository_name",
    "secret",
    "token",
}

NORMALIZED_UNSAFE_METADATA_ONLY_KEYS = {
    re.sub(r"[^0-9a-z]+", "", key.casefold()) for key in UNSAFE_METADATA_ONLY_KEYS
}

UNSAFE_METADATA_ONLY_KEY_TOKENS = {
    "credential": "credential",
    "credentials": "credential",
    "secret": "secret",
    "token": "token",
}

RAW_CONTEXT_KEYS = {"raw"}
RAW_CONTENT_DESCENDANT_KEYS = {
    "body",
    "completion",
    "content",
    "input",
    "message",
    "output",
    "request",
    "response",
    "text",
}

UNSAFE_METADATA_ONLY_KEY_PHRASES = (
    (("artifact", "body"), "artifact_body"),
    (("artifact", "example"), "artifact_example"),
    (("code", "excerpt"), "code_excerpt"),
    (("code", "snippet"), "code_snippet"),
    (("code", "text"), "code"),
    (("content", "excerpt"), "content_excerpt"),
    (("content", "example"), "content_example"),
    (("content", "summary"), "content_summary"),
    (("customer", "data"), "customer_data"),
    (("log", "excerpt"), "log_excerpt"),
    (("log", "text"), "log"),
    (("prompt", "text"), "prompt"),
    (("prompt", "example"), "prompt_example"),
    (("raw", "body"), "raw_body"),
    (("raw", "completion"), "raw_completion"),
    (("raw", "content"), "raw_content"),
    (("raw", "input"), "raw_input"),
    (("raw", "message"), "raw_message"),
    (("raw", "output"), "raw_output"),
    (("raw", "prompt"), "raw_prompt"),
    (("raw", "request"), "raw_request"),
    (("raw", "response"), "raw_response"),
    (("raw", "text"), "raw_text"),
    (("real", "path"), "real_path"),
    (("real", "repo"), "real_repo"),
    (("repo", "name"), "repo_name"),
    (("repository", "name"), "repository_name"),
)

TASK_HASH_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
EVENT_ID_RE = re.compile(r"^evt_[A-Za-z0-9_.-]+$")
PACKAGE_ID_RE = re.compile(r"^pkg_[0-9a-f]{12,64}$")
TAXONOMY_CODE_RE = re.compile(r"^[a-z][a-z0-9_]*(?:[._][a-z][a-z0-9_]*)+$")
MACHINE_ID_RE = re.compile(r"^anon-[A-Za-z0-9_.-]+$")
SHORT_REPO_IDENTIFIER_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,99}/[A-Za-z0-9][A-Za-z0-9_.-]{0,99}")
UNSAFE_METADATA_ONLY_VALUE_PATTERNS = (
    ("credential_url", re.compile(r"://[^/\s:@]+:[^@\s]+@")),
    ("credential", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,})\b")),
    ("real_path", re.compile(r"(?<![A-Za-z0-9])(?:/home/|/Users/|/private/|/var/log/|/etc/|[A-Za-z]:\\)[^\s,;]*")),
    ("real_repo", re.compile(r"\b(?:github|gitlab|bitbucket)\.com[:/][A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")),
)
REPO_CONTEXT_TOKENS = {"repo", "repository", "remote", "origin", "upstream"}
REPO_PRIVATE_KEY_TOKENS = {"repo", "repository", "private"}
SAFE_REPO_PRIVATE_METADATA_KEYS = {
    "repositories",
    "privateeventcount",
    "repohash",
    "repoidhash",
    "repositorycount",
}
SYNC_EXPORT_PACKAGE_KEYS = {
    "destination_hash",
    "event_count",
    "event_ids",
    "events",
    "mode",
    "package_id",
    "taxonomy_counts",
    "would_upload",
}


def normalize_metadata_key(key: Any) -> str:
    return re.sub(r"[^0-9a-z]+", "", str(key).casefold())


def tokenize_metadata_key(key: Any) -> list[str]:
    tokens: list[str] = []
    for part in re.sub(r"[^0-9A-Za-z]+", " ", str(key)).split():
        tokens.extend(
            match.group(0).casefold()
            for match in re.finditer(r"[A-Z]+(?=[A-Z][a-z]|\d|$)|[A-Z]?[a-z]+|\d+", part)
        )
    return [_singularize_token(token) for token in tokens]


def _singularize_token(token: str) -> str:
    if token.endswith("ies") and len(token) > 3:
        return f"{token[:-3]}y"
    if token.endswith("s") and len(token) > 1 and token not in {"credentials"}:
        return token[:-1]
    return token


def load_taxonomy(path: str | None) -> set[str]:
    if not path:
        return set()

    taxonomy: set[str] = set()
    current_category: str | None = None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith(" ") and stripped.endswith(":"):
            current_category = stripped[:-1]
            continue
        if current_category and stripped.startswith("- "):
            taxonomy.add(f"{current_category}.{stripped[2:].strip()}")
    return taxonomy


def events_from_json_value(path: str, value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        if not all(isinstance(item, dict) for item in value):
            raise ValueError(f"{path}: all array items must be event objects")
        return value
    if isinstance(value, dict):
        return [value]
    raise ValueError(f"{path}: event file must contain an object or array")


def load_events(path: str) -> list[dict[str, Any]]:
    text = Path(path).read_text(encoding="utf-8")
    if not text.strip():
        return []
    if path.endswith(".jsonl"):
        events: list[dict[str, Any]] = []
        for index, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{index}: event must be a JSON object")
            events.append(value)
        return events

    return events_from_json_value(path, json.loads(text))


def safe_package_field_name(key: Any) -> str:
    diagnostic = unsafe_metadata_key_diagnostic(key)
    if diagnostic and diagnostic != str(key):
        return diagnostic
    return str(key)


def validate_event_package(value: dict[str, Any], prefix: str | None = None) -> list[dict[str, Any]]:
    package_prefix = prefix or "package"
    errors: list[str] = []

    unknown_keys = sorted(set(value) - SYNC_EXPORT_PACKAGE_KEYS)
    for key in unknown_keys:
        errors.append(f"{package_prefix}: package contains unknown top-level field {safe_package_field_name(key)}")

    events = value.get("events")
    if not isinstance(events, list) or not all(isinstance(event, dict) for event in events):
        errors.append(f"{package_prefix}: package events must be an array of objects")
        events = []

    metadata = {key: child for key, child in value.items() if key != "events"}
    unsafe_fields = sorted(
        {
            diagnostic
            for key, parent_key, in_repo_context, in_raw_context in iter_key_contexts(metadata)
            if (diagnostic := unsafe_metadata_key_diagnostic(key, parent_key, in_repo_context, in_raw_context))
        }
    )
    for diagnostic in unsafe_fields:
        errors.append(f"{package_prefix}: package metadata contains unsafe field {diagnostic}")
    for path, string_value, field_name, in_repo_context, _in_raw_context in iter_string_values(metadata):
        reason = unsafe_metadata_value_reason(string_value, field_name, in_repo_context)
        if reason:
            errors.append(f"{package_prefix}: unsafe package metadata value at {path} ({reason})")

    if "mode" in value and value.get("mode") != "export":
        errors.append(f"{package_prefix}: package mode must be export")
    if "event_count" in value and (not isinstance(value.get("event_count"), int) or value.get("event_count") != len(events)):
        errors.append(f"{package_prefix}: package event_count must match events length")
    event_ids = value.get("event_ids")
    if "event_ids" in value:
        if not isinstance(event_ids, list) or not all(
            isinstance(event_id, str) and EVENT_ID_RE.match(event_id) for event_id in event_ids
        ):
            errors.append(f"{package_prefix}: package event_ids must be an array of safe evt_* identifiers")
        else:
            exported_event_ids = [event.get("event_id") for event in events]
            if event_ids != exported_event_ids:
                errors.append(f"{package_prefix}: package event_ids must match exported event event_id values")
    if "package_id" in value and (not isinstance(value.get("package_id"), str) or not PACKAGE_ID_RE.match(value.get("package_id"))):
        errors.append(f"{package_prefix}: package_id must match pkg_<12-64 lowercase hex>")
    destination_hash = value.get("destination_hash")
    if "destination_hash" in value and destination_hash is not None and (
        not isinstance(destination_hash, str) or not TASK_HASH_RE.match(destination_hash)
    ):
        errors.append(f"{package_prefix}: destination_hash must be null or match sha256:<64 lowercase hex>")
    taxonomy_counts = value.get("taxonomy_counts")
    if "taxonomy_counts" in value and not (
        isinstance(taxonomy_counts, dict)
        and all(
            isinstance(key, str) and TAXONOMY_CODE_RE.match(key) and isinstance(count, int)
            for key, count in taxonomy_counts.items()
        )
    ):
        errors.append(f"{package_prefix}: taxonomy_counts must be an object of safe taxonomy-code integer counts")
    if "would_upload" in value and not isinstance(value.get("would_upload"), bool):
        errors.append(f"{package_prefix}: would_upload must be a boolean")

    if errors:
        raise ValueError("; ".join(errors))
    return events


def load_event_input(path: str, package_error_prefix: str | None = None) -> list[dict[str, Any]]:
    if path.endswith(".jsonl"):
        return load_events(path)

    text = Path(path).read_text(encoding="utf-8")
    value = json.loads(text)
    if isinstance(value, dict) and "events" in value and not REQUIRED_FIELDS <= set(value):
        return validate_event_package(value, package_error_prefix)
    return events_from_json_value(path, value)


def is_likely_repo_context_key(key: Any) -> bool:
    return any(token in REPO_CONTEXT_TOKENS for token in tokenize_metadata_key(key))


def is_raw_context_key(key: Any) -> bool:
    return normalize_metadata_key(key) in RAW_CONTEXT_KEYS


def raw_content_descendant_reason(key: Any, in_raw_context: bool = False) -> str | None:
    if not in_raw_context:
        return None
    tokens = tokenize_metadata_key(key)
    if len(tokens) == 1 and tokens[0] in RAW_CONTENT_DESCENDANT_KEYS:
        return f"raw_{tokens[0]}"
    return None


def short_repo_identifier_reason(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    if not SHORT_REPO_IDENTIFIER_RE.fullmatch(value):
        return None
    if not re.search(r"[A-Za-z]", value):
        return None
    return "real_repo"


def short_repo_identifier_fragment_reason(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    match = SHORT_REPO_IDENTIFIER_RE.search(value)
    if not match:
        return None
    if not re.search(r"[A-Za-z]", match.group(0)):
        return None
    return "real_repo"


def unsafe_taxonomy_code_reason(value: str) -> str | None:
    if TAXONOMY_CODE_RE.fullmatch(value):
        return None
    return short_repo_identifier_reason(value) or unsafe_metadata_value_reason(value) or "invalid_format"


def unsafe_dynamic_key_reason(
    key: Any,
    parent_key: Any | None = None,
    in_repo_context: bool = False,
) -> str | None:
    string_key = str(key)
    string_pattern_reason = unsafe_metadata_value_reason(string_key)
    if string_pattern_reason:
        return string_pattern_reason
    short_repo_reason = short_repo_identifier_reason(string_key)
    if short_repo_reason:
        return short_repo_reason
    return None


def unsafe_metadata_key_fragment_reason(key: Any) -> str | None:
    string_key = str(key)
    for reason, pattern in UNSAFE_METADATA_ONLY_VALUE_PATTERNS:
        if pattern.search(string_key):
            return reason
    return short_repo_identifier_fragment_reason(string_key)


def conservative_repo_private_key_reason(key: Any) -> str | None:
    if normalize_metadata_key(key) in SAFE_REPO_PRIVATE_METADATA_KEYS:
        return None
    tokens = tokenize_metadata_key(key)
    if not any(token in REPO_PRIVATE_KEY_TOKENS for token in tokens):
        return None
    string_key = str(key)
    for reason, pattern in UNSAFE_METADATA_ONLY_VALUE_PATTERNS:
        if pattern.search(string_key):
            return reason
    if short_repo_identifier_fragment_reason(string_key):
        return "real_repo"
    if "repo" in tokens or "repository" in tokens:
        return "real_repo"
    return "private"


def unsafe_metadata_key_phrase_reason(key: Any) -> tuple[str, bool] | None:
    tokens = tokenize_metadata_key(key)
    for phrase, reason in UNSAFE_METADATA_ONLY_KEY_PHRASES:
        for index in range(0, len(tokens) - len(phrase) + 1):
            if tuple(tokens[index : index + len(phrase)]) == phrase:
                phrase_is_whole_key = len(tokens) == len(phrase)
                return reason, not phrase_is_whole_key
    return None


def unsafe_metadata_key_phrase_requires_sanitized_diagnostic(key: Any) -> bool:
    tokens = tokenize_metadata_key(key)
    for phrase, _reason in UNSAFE_METADATA_ONLY_KEY_PHRASES:
        for index in range(0, len(tokens) - len(phrase) + 1):
            if tuple(tokens[index : index + len(phrase)]) != phrase:
                continue
            suffix_tokens = tokens[:index] + tokens[index + len(phrase) :]
            if suffix_tokens and any(token in REPO_CONTEXT_TOKENS or token == "private" for token in suffix_tokens):
                return True
    return False


def iter_key_contexts(
    value: Any,
    parent_key: Any | None = None,
    in_repo_context: bool = False,
    in_raw_context: bool = False,
) -> list[tuple[str, Any | None, bool, bool]]:
    keys: list[tuple[str, Any | None, bool, bool]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            keys.append((str(key), parent_key, in_repo_context, in_raw_context))
            child_repo_context = in_repo_context or is_likely_repo_context_key(key)
            child_raw_context = in_raw_context or is_raw_context_key(key)
            keys.extend(iter_key_contexts(child, key, child_repo_context, child_raw_context))
    elif isinstance(value, list):
        for child in value:
            keys.extend(iter_key_contexts(child, parent_key, in_repo_context, in_raw_context))
    return keys


def unsafe_metadata_key_reason(
    key: Any,
    parent_key: Any | None = None,
    in_repo_context: bool = False,
    in_raw_context: bool = False,
) -> str | None:
    raw_reason = raw_content_descendant_reason(key, in_raw_context)
    if raw_reason:
        return raw_reason
    normalized = normalize_metadata_key(key)
    if normalized in NORMALIZED_UNSAFE_METADATA_ONLY_KEYS:
        return str(key)
    phrase_reason = unsafe_metadata_key_phrase_reason(key)
    if phrase_reason:
        reason, _is_composite = phrase_reason
        return reason
    dynamic_reason = unsafe_dynamic_key_reason(key, parent_key, in_repo_context)
    if dynamic_reason:
        return dynamic_reason
    repo_private_reason = conservative_repo_private_key_reason(key)
    if repo_private_reason:
        return repo_private_reason
    tokens = tokenize_metadata_key(key)
    for token in tokens:
        if token in UNSAFE_METADATA_ONLY_KEY_TOKENS:
            return UNSAFE_METADATA_ONLY_KEY_TOKENS[token]
    return None


def unsafe_metadata_key_diagnostic(
    key: Any,
    parent_key: Any | None = None,
    in_repo_context: bool = False,
    in_raw_context: bool = False,
) -> str | None:
    reason = unsafe_metadata_key_reason(key, parent_key, in_repo_context, in_raw_context)
    if not reason:
        return None
    if raw_content_descendant_reason(key, in_raw_context):
        return reason
    phrase_reason = unsafe_metadata_key_phrase_reason(key)
    if phrase_reason:
        _phrase_label, is_composite = phrase_reason
        if is_composite and unsafe_metadata_key_phrase_requires_sanitized_diagnostic(key):
            return f"unsafe key ({reason})"
    if (
        conservative_repo_private_key_reason(key) == reason
        and not in_repo_context
        and not (parent_key is not None and is_likely_repo_context_key(parent_key))
        and not unsafe_metadata_value_reason(str(key))
    ):
        return f"unsafe key ({reason})"
    if unsafe_dynamic_key_reason(key, parent_key, in_repo_context):
        return f"unsafe dynamic key ({reason})"
    if unsafe_metadata_key_fragment_reason(key):
        return f"unsafe key ({reason})"
    return str(key)


def unsafe_metadata_value_reason(value: Any, field_name: Any | None = None, in_repo_context: bool = False) -> str | None:
    if not isinstance(value, str):
        return None
    for reason, pattern in UNSAFE_METADATA_ONLY_VALUE_PATTERNS:
        if pattern.search(value):
            return reason
    if in_repo_context or (field_name is not None and is_likely_repo_context_key(field_name)):
        return short_repo_identifier_reason(value)
    return None


def safe_metadata_path_key(
    key: Any,
    parent_key: Any | None = None,
    in_repo_context: bool = False,
    in_raw_context: bool = False,
) -> str:
    diagnostic = unsafe_metadata_key_diagnostic(key, parent_key, in_repo_context, in_raw_context)
    if diagnostic and diagnostic != str(key):
        return "<unsafe-key>"
    return str(key)


def iter_string_values(
    value: Any,
    path: str = "$",
    field_name: Any | None = None,
    in_repo_context: bool = False,
    in_raw_context: bool = False,
) -> list[tuple[str, str, Any | None, bool, bool]]:
    values: list[tuple[str, str, Any | None, bool, bool]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_repo_context = in_repo_context or is_likely_repo_context_key(key)
            child_raw_context = in_raw_context or is_raw_context_key(key)
            values.extend(
                iter_string_values(
                    child,
                    f"{path}.{safe_metadata_path_key(key, field_name, in_repo_context, in_raw_context)}",
                    key,
                    child_repo_context,
                    child_raw_context,
                )
            )
    elif isinstance(value, list):
        for index, child in enumerate(value):
            values.extend(iter_string_values(child, f"{path}[{index}]", field_name, in_repo_context, in_raw_context))
    elif isinstance(value, str):
        values.append((path, value, field_name, in_repo_context, in_raw_context))
    return values


def validate_timestamp(value: Any, errors: list[str], prefix: str) -> None:
    if not isinstance(value, str):
        errors.append(f"{prefix}: timestamp must be a string")
        return
    candidate = value.replace("Z", "+00:00")
    try:
        datetime.fromisoformat(candidate)
    except ValueError:
        errors.append(f"{prefix}: timestamp is not ISO-8601 date-time")


def validate_skill_pack(value: Any, errors: list[str], prefix: str) -> None:
    if not isinstance(value, dict):
        errors.append(f"{prefix}: skill_pack must be an object")
        return
    has_valid_identity = False
    for field_name in ("release", "source_commit"):
        if field_name not in value:
            continue
        field_value = value[field_name]
        if not isinstance(field_value, str) or not field_value.strip():
            errors.append(f"{prefix}: skill_pack {field_name} must be a non-empty string")
        elif field_value == "unknown":
            errors.append(f"{prefix}: skill_pack {field_name} must not be unknown")
        else:
            has_valid_identity = True
    if not has_valid_identity:
        errors.append(f"{prefix}: skill_pack requires release or source_commit")


def validate_machine_id(value: Any, errors: list[str], prefix: str) -> None:
    if not isinstance(value, str) or not MACHINE_ID_RE.match(value):
        errors.append(f"{prefix}: machine_id must be pseudonymous and start with anon-")
        return
    hostname = socket.gethostname()
    if hostname and value.casefold() == hostname.casefold():
        errors.append(f"{prefix}: machine_id must not be derived from hostname")


def validate_event(event: dict[str, Any], taxonomy: set[str], prefix: str) -> list[str]:
    errors: list[str] = []

    missing = sorted(REQUIRED_FIELDS - set(event))
    for field in missing:
        errors.append(f"{prefix}: missing required field {field}")

    if event.get("schema_version") != "1.0.0":
        errors.append(f"{prefix}: schema_version must be 1.0.0")
    if not isinstance(event.get("event_id"), str) or not EVENT_ID_RE.match(str(event.get("event_id"))):
        errors.append(f"{prefix}: event_id must match evt_*")
    if event.get("event") not in EVENT_TYPES:
        errors.append(f"{prefix}: event must be one of {sorted(EVENT_TYPES)}")
    validate_timestamp(event.get("timestamp"), errors, prefix)
    if event.get("privacy_mode") not in {"metadata_only", "redacted_content_opt_in"}:
        errors.append(f"{prefix}: privacy_mode must be metadata_only or redacted_content_opt_in")
    validate_machine_id(event.get("machine_id"), errors, prefix)
    validate_skill_pack(event.get("skill_pack"), errors, prefix)

    if not isinstance(event.get("status"), str):
        errors.append(f"{prefix}: status must be a string")

    task_hash = event.get("task_hash")
    if not isinstance(task_hash, str) or not TASK_HASH_RE.match(task_hash):
        errors.append(f"{prefix}: task_hash must match sha256:<64 lowercase hex>")

    taxonomy_codes = event.get("taxonomy_codes", [])
    if taxonomy_codes is None:
        taxonomy_codes = []
    if not isinstance(taxonomy_codes, list) or not all(isinstance(code, str) for code in taxonomy_codes):
        errors.append(f"{prefix}: taxonomy_codes must be an array of strings")
    else:
        unsafe_codes = {
            reason
            for code in taxonomy_codes
            if (reason := unsafe_taxonomy_code_reason(code))
        }
        for reason in sorted(unsafe_codes):
            errors.append(f"{prefix}: taxonomy_codes contains unsafe taxonomy code ({reason})")
        unknown = sorted({code for code in taxonomy_codes if TAXONOMY_CODE_RE.fullmatch(code)} - taxonomy)
        if not taxonomy:
            unknown = []
        for code in unknown:
            errors.append(f"{prefix}: unknown taxonomy code {code}")

    privacy_mode = event.get("privacy_mode")
    if privacy_mode in {"metadata_only", "redacted_content_opt_in"}:
        unsafe = sorted(
            ({"events"} if "events" in event else set())
            | {
                diagnostic
                for key, parent_key, in_repo_context, in_raw_context in iter_key_contexts(event)
                if (diagnostic := unsafe_metadata_key_diagnostic(key, parent_key, in_repo_context, in_raw_context))
            }
        )
        for diagnostic in unsafe:
            errors.append(f"{prefix}: {privacy_mode} event contains unsafe field {diagnostic}")
        for path, value, field_name, in_repo_context, _in_raw_context in iter_string_values(event):
            reason = unsafe_metadata_value_reason(value, field_name, in_repo_context)
            if reason:
                if privacy_mode == "metadata_only":
                    errors.append(f"{prefix}: unsafe metadata-only value at {path} ({reason})")
                else:
                    errors.append(f"{prefix}: unsafe redacted_content_opt_in value at {path} ({reason})")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="JSON or JSONL event files")
    parser.add_argument("--taxonomy", help="Failure taxonomy YAML path")
    args = parser.parse_args()

    taxonomy = load_taxonomy(args.taxonomy)
    all_errors: list[str] = []
    total_events = 0

    for path in args.paths:
        try:
            events = load_event_input(path, package_error_prefix=path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            all_errors.append(f"{path}: {exc}")
            continue
        for index, event in enumerate(events, start=1):
            total_events += 1
            all_errors.extend(validate_event(event, taxonomy, f"{path}:{index}"))

    if all_errors:
        for error in all_errors:
            print(f"ERROR: {error}")
        return 2

    print(f"validated {total_events} event{'s' if total_events != 1 else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
