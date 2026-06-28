# Historical Bootstrap Run

This directory is retained as historical implementation evidence for the information sufficiency gate bootstrap.

It is non-authoritative for new control runs. The `requirements.control.json` file uses schema version `1.0`, predates the current `information_sufficiency_check` contract, and predates run-local counterexample review evidence binding.

New runs must use the current requirements schema, include `approved_control.information_sufficiency_check`, bind independent counterexample review evidence to run-local JSON, and pass the current guard/runtime validators.
