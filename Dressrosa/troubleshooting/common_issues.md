# Common Issues

This document lists common installation and execution issues for Dressrosa, including fixes.

## 1) ModuleNotFoundError: No module named 'itsdangerous'
Cause:
- Missing dependency required by `SessionMiddleware`.

Fix:
1. Ensure `itsdangerous` is present in `requirements.txt`.
2. Reinstall dependencies:
   - `pip install -r requirements.txt`

## 2) configparser.MissingSectionHeaderError in `alembic.ini` with BOM prefix before `[alembic]`
Cause:
- `alembic.ini` was saved with UTF-8 BOM.

Fix:
1. Save `alembic.ini` as UTF-8 without BOM.
2. Re-run migration:
   - `alembic upgrade head`

## 3) ModuleNotFoundError: No module named 'sqlalchemy' while using `py -3`
Cause:
- `py -3` may run a global interpreter instead of the active venv interpreter.

Fix:
1. Activate venv.
2. Use `python` (not `py -3`) for project commands.
3. Reinstall dependencies if needed:
   - `pip install -r requirements.txt`

## 4) ModuleNotFoundError: No module named 'app' when running seed script
Cause:
- Running script by file path changes import resolution.

Fix:
1. Run seed script as module from `Dressrosa` root:
   - `python -m scripts.seed_initial_data`

## 5) ValueError: password cannot be longer than 72 bytes
Cause:
- Compatibility issue between `passlib==1.7.4` and newer `bcrypt`.

Fix:
1. Pin `bcrypt==4.0.1` in `requirements.txt`.
2. Reinstall dependencies:
   - `pip install -r requirements.txt`

## 6) sqlalchemy.exc.OperationalError: no such table: users
Cause:
- Database schema not migrated, or wrong working directory DB file.

Fix:
1. From `Dressrosa` folder, run:
   - `alembic upgrade head`
2. Seed data:
   - `python -m scripts.seed_initial_data`
3. Confirm app runs from the same project directory.

## 7) Uvicorn command fails with `No module named uvicorn`
Cause:
- Dependencies are not installed in the active environment.

Fix:
1. Activate venv.
2. Install dependencies:
   - `pip install -r requirements.txt`

## 8) Local database files showing in git status
Cause:
- SQLite runtime files are local artifacts.

Fix:
1. Do not commit `dressrosa.db` files.
2. Keep them local-only for development/testing.
