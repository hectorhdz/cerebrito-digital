# Product Backlog

| Backlog ID | Epic | Feature | Description | Target Sprint | Status | Notes |
|---|---|---|---|---|---|---|
| BL-001 | Platform Foundation | FastAPI skeleton | Initialize FastAPI project structure with modular monolith layout. | Sprint 1 | Completed | Implemented on `dressrosa-sprint1` |
| BL-002 | Platform Foundation | Data layer bootstrap | Configure SQLAlchemy models and Alembic migration baseline. | Sprint 1 | Completed | Added SQLAlchemy models + Alembic baseline migration |
| BL-003 | Platform Foundation | App configuration | Implement configuration, logging, and environment separation. | Sprint 1 | Completed | Added env-separated settings, logging config, and env files |
| BL-004 | Platform Foundation | Auth primitives | Add password hashing, web session auth, and API token auth foundations. | Sprint 2 | Completed | Added bcrypt hashing, JWT (2h), API auth endpoints, and web session login/logout |
| BL-005 | Platform Foundation | Initial seed data | Seed default roles and initial admin user. | Sprint 2 | Completed | Added idempotent seed script with default admin and role assignment |
| BL-006 | Users and Access | User CRUD | User CRUD for HR/Admin. | Sprint 3 | Planned | Not started |
| BL-007 | Users and Access | Role assignment | Role assignment management. | Sprint 3 | Planned | Not started |
| BL-008 | Users and Access | Org mapping | Manager-employee relationship management. | Sprint 3 | Planned | Not started |
| BL-009 | Users and Access | Profile endpoints | Profile and account status endpoints. | Sprint 3 | Planned | Not started |
| BL-010 | Users and Access | Authorization guards | Role guards for web routes and REST endpoints. | Sprint 2 | Planned | Not started |
| BL-011 | Leave Taxonomy and Policies | Leave types | Leave type management (`paid`, `unpaid`, `holiday_substitution`). | Sprint 4 | Planned | Config-driven |
| BL-012 | Leave Taxonomy and Policies | Leave subtypes | Leave subtype management for scalable subtype sets. | Sprint 4 | Planned | Config-driven |
| BL-013 | Leave Taxonomy and Policies | Policy model | Policy placeholders for entitlement/accrual rules. | Sprint 4 | Planned | Extensible model |
| BL-014 | Leave Taxonomy and Policies | Subtype validation | Validation rules per subtype. | Sprint 4 | Planned | Rule hooks |
| BL-015 | Leave Requests and Approvals | Leave submission | Employee leave request submission. | Sprint 4 | Planned | Not started |
| BL-016 | Leave Requests and Approvals | Request lifecycle | Request statuses (`pending`, `approved`, `declined`, `cancelled`). | Sprint 4 | Planned | Not started |
| BL-017 | Leave Requests and Approvals | Manager decisions | Manager approval/decline actions. | Sprint 5 | Planned | Not started |
| BL-018 | Leave Requests and Approvals | HR override | HR override/super-approval actions. | Sprint 5 | Planned | Not started |
| BL-019 | Leave Requests and Approvals | Approval timeline | Approval history timeline view and API. | Sprint 5 | Planned | Not started |
| BL-020 | Leave Balance Ledger and Reporting | Balance ledger | Ledger events (`accrual`, `reservation`, `consumption`, `reversal`, `adjustment`). | Sprint 7 | Planned | Not started |
| BL-021 | Leave Balance Ledger and Reporting | Balance projections | Current, upcoming, pending, and consumed leave projections. | Sprint 7 | Planned | Not started |
| BL-022 | Leave Balance Ledger and Reporting | Employee summary | Employee leave summary endpoint and page. | Sprint 7 | Planned | Not started |
| BL-023 | Leave Balance Ledger and Reporting | HR reporting | HR reporting page and team/company API snapshots. | Sprint 7 | Planned | Not started |
| BL-024 | Attendance and Corrections | Clock-in | Daily single clock-in endpoint and page. | Sprint 6 | Planned | One stamp-in per day |
| BL-025 | Attendance and Corrections | Clock-out | Daily single clock-out endpoint and page. | Sprint 6 | Planned | One stamp-out per day |
| BL-026 | Attendance and Corrections | Daily uniqueness | Unique constraint by employee/date. | Sprint 6 | Planned | Not started |
| BL-027 | Attendance and Corrections | Attendance correction | Authorized attendance correction flow. | Sprint 6 | Planned | Manager/HR edit with reason |
| BL-028 | Attendance and Corrections | Attendance audit | Attendance audit/history view. | Sprint 6 | Planned | Not started |
| BL-029 | UX and Workflow Reliability | Employee dashboard | Employee dashboard for daily status and requests. | Sprint 7 | Planned | Not started |
| BL-030 | UX and Workflow Reliability | Manager dashboard | Manager dashboard for team request queue. | Sprint 7 | Planned | Not started |
| BL-031 | UX and Workflow Reliability | HR dashboard | HR dashboard for override queue and metrics. | Sprint 7 | Planned | Not started |
| BL-032 | UX and Workflow Reliability | UX feedback | Validation and user feedback messages. | Sprint 7 | Planned | Not started |
| BL-033 | Quality and Release Readiness | Unit tests | Unit tests for core services. | Sprint 8 | Planned | Not started |
| BL-034 | Quality and Release Readiness | Integration tests | Integration tests for critical workflows. | Sprint 8 | Planned | Not started |
| BL-035 | Quality and Release Readiness | API docs hardening | API documentation hardening and examples. | Sprint 8 | Planned | Not started |
| BL-036 | Quality and Release Readiness | DB migration notes | Migration path notes SQLite -> PostgreSQL. | Sprint 8 | Planned | Not started |
| BL-037 | Quality and Release Readiness | Security checklist | Security checklist before launch auth enhancements. | Sprint 8 | Planned | Not started |
