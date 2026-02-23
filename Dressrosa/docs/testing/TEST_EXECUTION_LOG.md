# Dressrosa Test Execution Log

This file tracks test cases that were executed, including outcome and context.

| Test Case ID | Test Case | Description | Command/Method | Status | Result Summary |
|---|---|---|---|---|---|
| TC-BL001-001 | Health endpoint smoke test | Validate that `/api/v1/health` returns HTTP 200 and `{ "status": "ok" }`. | `py -3 -m pytest Dressrosa/tests -q` | Blocked | Execution failed because `pytest` is not installed in the active Python environment (`No module named pytest`). |
| TC-BL002-001 | DB health endpoint smoke test | Validate that `/api/v1/health/db` returns HTTP 200 and confirms DB reachability. | `py -3 -m pytest Dressrosa/tests -q` | Blocked | Not yet runnable in current environment because `pytest` is not installed. |
| TC-BL003-001 | Environment selection test | Validate that `test` environment resolves `.env.test`. | `py -3 -m pytest Dressrosa/tests -q` | Blocked | Not yet runnable in current environment because `pytest` is not installed. |
| TC-BL003-002 | Production env selection test | Validate that `production` environment resolves `.env.prod`. | `py -3 -m pytest Dressrosa/tests -q` | Blocked | Not yet runnable in current environment because `pytest` is not installed. |
| TC-BL004-001 | Password hashing test | Validate password hashing and verification round-trip behavior. | `py -3 -m pytest Dressrosa/tests -q` | Blocked | Not yet runnable in current environment because `pytest` is not installed. |
| TC-BL004-002 | JWT issuance test | Validate issued token includes subject and 2-hour expiry (`7200` seconds). | `py -3 -m pytest Dressrosa/tests -q` | Blocked | Not yet runnable in current environment because `pytest` is not installed. |

## Notes
- Automated tests exist at `Dressrosa/tests/test_health.py`, `Dressrosa/tests/test_config.py`, and `Dressrosa/tests/test_auth_security.py`.
- After creating and activating a virtual environment and installing `Dressrosa/requirements.txt`, rerun:
  - `py -3 -m pytest Dressrosa/tests -q`
- Update this log with final test outcomes (`Passed`/`Failed`) after rerun.
