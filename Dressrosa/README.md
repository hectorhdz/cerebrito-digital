# Dressrosa

HR management web app for leave requests, attendance tracking, and manager approvals.

## Sprint 1 Status
- BL-001 implemented: FastAPI skeleton with modular monolith layout.
- BL-002 implemented: SQLAlchemy foundation and Alembic baseline migration.
- BL-003 implemented: environment-separated configuration and centralized logging.

## Documentation
- Project plan: `docs/PROJECT_PLAN.md`
- Backlog: `docs/backlog/PRODUCT_BACKLOG.md`
- Sprint roadmap: `docs/backlog/SPRINT_ROADMAP.md`
- Architecture diagrams (rendered images): `docs/Architecture.md`
- Test execution log: `docs/testing/TEST_EXECUTION_LOG.md`

## Installation Requirements (Windows)
- Windows 10 or Windows 11
- Python 3.11+ with `py` launcher available
- PowerShell 5.1+ or PowerShell 7+
- Git (recommended)

## Environment Files
- `.env`: development defaults
- `.env.test`: test settings
- `.env.prod`: production settings
- `.env.example`: template reference

The app chooses environment files based on `ENVIRONMENT`:
- `development` -> `.env`
- `test` -> `.env` + `.env.test`
- `production` -> `.env` + `.env.prod`

## Local Setup and Run (Windows Workstation)
Run all commands from repository root (`c:\Users\webit\Documents\Github\cerebrito-digital`).

1. Move into the project folder:
   - `cd Dressrosa`
2. Create a virtual environment:
   - `py -3 -m venv .venv`
3. Allow local script execution for current shell session (if needed):
   - `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
4. Activate virtual environment:
   - `.\.venv\Scripts\Activate.ps1`
5. Upgrade pip:
   - `python -m pip install --upgrade pip`
6. Install dependencies:
   - `pip install -r requirements.txt`
7. Optional: select environment for this session:
   - `$env:ENVIRONMENT = "development"`
   - `$env:ENVIRONMENT = "test"`
   - `$env:ENVIRONMENT = "production"`
8. Apply database migrations:
   - `alembic upgrade head`
9. Run the application:
   - `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
10. Open the app in browser:
   - `http://127.0.0.1:8000/`
11. API health checks:
   - `http://127.0.0.1:8000/api/v1/health`
   - `http://127.0.0.1:8000/api/v1/health/db`
12. Run tests:
   - `pytest`

## Common Windows Troubleshooting
- If `py` is not recognized: reinstall Python and enable "Add Python to PATH".
- If venv activation fails: run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in the same PowerShell session.
- If `alembic` is not found: confirm venv is activated, then run `python -m alembic upgrade head`.
- If port 8000 is in use: run with another port, for example `--port 8001`.

## Notes About Diagram Rendering
The rendered diagrams in `docs/Architecture.md` use the PlantUML proxy service and fetch source from this repository.
If the default branch changes, update the branch name in diagram URLs.
