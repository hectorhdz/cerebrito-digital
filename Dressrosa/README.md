# Dressrosa

HR management web app for leave requests, attendance tracking, and manager approvals.

## Sprint Status
- Sprint 1: BL-001, BL-002, BL-003 implemented.
- Sprint 2: BL-004, BL-005, and BL-010 implemented.
- Sprint 3: BL-006 and BL-007 implemented (BL-008/BL-009 pending).

## Documentation
- Project plan: `docs/PROJECT_PLAN.md`
- Backlog: `docs/backlog/PRODUCT_BACKLOG.md`
- Sprint roadmap: `docs/backlog/SPRINT_ROADMAP.md`
- Architecture diagrams (rendered images): `docs/Architecture.md`
- Test execution log: `docs/testing/TEST_EXECUTION_LOG.md`
- Troubleshooting guide: `troubleshooting/common_issues.md`

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
9. Seed default data (roles + admin):
   - `python -m scripts.seed_initial_data`
10. Run the application:
   - `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
11. Open the app in browser:
   - `http://127.0.0.1:8000/`
12. API health checks:
   - `http://127.0.0.1:8000/api/v1/health`
   - `http://127.0.0.1:8000/api/v1/health/db`
13. Run tests:
   - `python -m pytest tests -q`

## Default Seed Credentials (BL-005)
- Username: `admin`
- Email: `admin@dressrosa.local`
- Password: `Test123`

Change this password immediately in non-local environments.

## Auth Endpoints (BL-004)
- API token login: `POST /api/v1/auth/token` with form fields `username` and `password`
- API current user: `GET /api/v1/auth/me` with `Authorization: Bearer <token>`
- Web login page: `GET /login`
- Web login submit: `POST /login`
- Web logout: `POST /logout`

## Role Guard Verification Endpoints (BL-010)
- API (requires bearer token + role):
  - `GET /api/v1/access/employee`
  - `GET /api/v1/access/manager`
  - `GET /api/v1/access/hr`
  - `GET /api/v1/access/admin`
- Web (requires session + role):
  - `GET /portal/employee`
  - `GET /portal/manager`
  - `GET /portal/hr`
  - `GET /portal/admin`

## User CRUD and Role Assignment Endpoints (BL-006/BL-007)
- API (HR/Admin only):
  - `GET /api/v1/users`
  - `POST /api/v1/users`
  - `GET /api/v1/users/{user_id}`
  - `PUT /api/v1/users/{user_id}`
  - `DELETE /api/v1/users/{user_id}`
  - `GET /api/v1/users/roles`
  - `POST /api/v1/users/{user_id}/roles`
  - `DELETE /api/v1/users/{user_id}/roles/{role_name}`
- Web (HR/Admin only):
  - `GET /users`
  - `POST /users`
  - `POST /users/{user_id}/delete`
  - `POST /users/{user_id}/roles`
  - `POST /users/{user_id}/roles/{role_name}/remove`

Role inheritance enabled by default:
- `admin` inherits `hr`, `manager`, `employee`
- `hr` inherits `manager`, `employee`
- `manager` inherits `employee`

Token/session duration is configured at `ACCESS_TOKEN_EXPIRE_MINUTES` and defaults to 120 minutes.

For known installation/runtime issues, see `troubleshooting/common_issues.md`.

## Common Windows Troubleshooting
- If `py` is not recognized: reinstall Python and enable "Add Python to PATH".
- If venv activation fails: run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in the same PowerShell session.
- If `alembic` is not found: confirm venv is activated, then run `python -m alembic upgrade head`.
- If port 8000 is in use: run with another port, for example `--port 8001`.

## Notes About Diagram Rendering
The rendered diagrams in `docs/Architecture.md` use the PlantUML proxy service and fetch source from this repository.
If the default branch changes, update the branch name in diagram URLs.
