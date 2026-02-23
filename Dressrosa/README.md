# Dressrosa

HR management web app for leave requests, attendance tracking, and manager approvals.

## Sprint 1 Status
- BL-001 implemented: FastAPI skeleton with modular monolith layout.

## Documentation
- Project plan: `docs/PROJECT_PLAN.md`
- Backlog: `docs/backlog/PRODUCT_BACKLOG.md`
- Sprint roadmap: `docs/backlog/SPRINT_ROADMAP.md`
- Architecture diagrams (rendered images): `docs/Architecture.md`

## Local Development (venv + requirements)
1. Create virtual environment:
   - `py -3 -m venv .venv`
2. Activate virtual environment (PowerShell):
   - `.\.venv\Scripts\Activate.ps1`
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Run API server:
   - `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
5. Open app:
   - `http://127.0.0.1:8000/`
6. Run tests:
   - `pytest`

## Notes About Diagram Rendering
The rendered diagrams in `docs/Architecture.md` use the PlantUML proxy service and fetch source from this repository.
If the default branch changes, update the branch name in diagram URLs.
