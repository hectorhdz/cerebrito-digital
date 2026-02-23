# Dressrosa Test Execution Log

This file tracks test cases that were executed, including outcome and context.

| Test Case ID | Test Case | Description | Command/Method | Status | Result Summary |
|---|---|---|---|---|---|
| TC-BL001-001 | Health endpoint smoke test | Validate that `/api/v1/health` returns HTTP 200 and `{ "status": "ok" }`. | `python -m pytest tests -q` | Blocked | Execution failed because `pytest` was not installed in the active Python environment. |
| TC-BL002-001 | DB health endpoint smoke test | Validate that `/api/v1/health/db` returns HTTP 200 and confirms DB reachability. | `python -m pytest tests -q` | Blocked | Not yet runnable in current environment because dependencies were not fully installed. |
| TC-BL003-001 | Environment selection test | Validate that `test` environment resolves `.env.test`. | `python -m pytest tests -q` | Blocked | Not yet runnable in current environment because dependencies were not fully installed. |
| TC-BL003-002 | Production env selection test | Validate that `production` environment resolves `.env.prod`. | `python -m pytest tests -q` | Blocked | Not yet runnable in current environment because dependencies were not fully installed. |
| TC-BL004-001 | Password hashing test | Validate password hashing and verification round-trip behavior. | `python -m pytest tests -q` | Blocked | Not yet runnable in current environment because dependencies were not fully installed. |
| TC-BL004-002 | JWT issuance test | Validate issued token includes subject and 2-hour expiry (`7200` seconds). | `python -m pytest tests -q` | Blocked | Not yet runnable in current environment because dependencies were not fully installed. |
| TC-BL005-001 | Seed roles/admin script | Validate seed script creates default roles and initial admin user idempotently. | `python -m scripts.seed_initial_data` | Not Run | Pending local execution after migrations are applied. |
| TC-BL010-001 | Role hierarchy expansion test | Validate admin/hr/manager inheritance logic for role guards. | `python -m pytest tests/test_role_guards.py -q` | Not Run | Added tests; pending execution in fully prepared local environment. |

## Notes
- Automated tests exist in `tests/`.
- Seed script exists at `scripts/seed_initial_data.py`.
- After dependencies are installed, rerun:
  - `python -m pytest tests -q`
- After applying migrations, run seed:
  - `python -m scripts.seed_initial_data`
- Update this log with final outcomes (`Passed`/`Failed`) after rerun.
