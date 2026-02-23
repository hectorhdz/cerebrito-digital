# Product Backlog

## Epic 1: Platform Foundation
1. Initialize FastAPI project structure with modular monolith layout.
2. Configure SQLAlchemy models + Alembic migration baseline.
3. Implement configuration, logging, and environment separation.
4. Add auth primitives (password hashing, sessions, API tokens).
5. Seed default roles and initial admin user.

## Epic 2: Users and Access
1. User CRUD for HR/Admin.
2. Role assignment management.
3. Manager-employee relationship management.
4. Profile and account status endpoints.
5. Authorization guards for web routes and REST endpoints.

## Epic 3: Leave Taxonomy and Policies
1. Leave type management (`paid`, `unpaid`, `holiday_substitution`).
2. Leave subtype management (configurable extensions).
3. Policy placeholders for entitlement/accrual rules.
4. Validation rules per subtype (future extensibility).

## Epic 4: Leave Requests and Approvals
1. Employee leave request submission.
2. Request status lifecycle (`pending`, `approved`, `declined`, `cancelled`).
3. Manager approval/decline actions.
4. HR override/super-approval actions.
5. Approval history timeline view.

## Epic 5: Leave Balance Ledger and Reporting
1. Ledger events (`accrual`, `reservation`, `consumption`, `reversal`, `adjustment`).
2. Balance projections (current, upcoming, pending, consumed).
3. Employee leave summary endpoint and page.
4. HR reporting page and API for team/company snapshots.

## Epic 6: Attendance and Corrections
1. Daily single clock-in endpoint and page.
2. Daily single clock-out endpoint and page.
3. Unique constraint by employee/date.
4. Authorized attendance correction flow.
5. Attendance audit/history view.

## Epic 7: UX and Workflow Reliability
1. Employee dashboard (today status, pending requests).
2. Manager dashboard (team requests queue).
3. HR dashboard (override queue, global metrics).
4. Validation and user feedback messages.

## Epic 8: Quality and Release Readiness
1. Unit tests for services.
2. Integration tests for critical workflows.
3. API docs hardening and examples.
4. Migration path notes SQLite -> PostgreSQL.
5. Security checklist before launch auth enhancements.
