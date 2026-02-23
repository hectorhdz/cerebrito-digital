# Sprint Roadmap

| Sprint | Goal | Deliverables | Verification | Status | Notes |
|---|---|---|---|---|---|
| Sprint 0 | Planning baseline | Project plan; architecture UML; ER diagram; workflow sequence diagrams; product backlog; sprint roadmap | Docs present and reviewed | Completed | Baseline planning delivered |
| Sprint 1 | Project bootstrap | FastAPI app skeleton; config/dependency management; SQLAlchemy base models; Alembic init; health endpoint; base layout page | App boots locally; initial migration applies | Completed | BL-001, BL-002, BL-003 completed and merged |
| Sprint 2 | Auth and roles | Login/logout; password hashing; session auth; API token/JWT auth; role guards | Protected endpoints enforce roles; auth tests pass | In Progress | BL-004, BL-005, BL-010 merged; full test verification still pending |
| Sprint 3 | Users and organization | User CRUD; role assignment; employee-manager mapping | Admin/HR user management works; relationships query correctly | In Progress | BL-006, BL-007, and BL-008 completed; BL-009 pending |
| Sprint 4 | Leave taxonomy and requests | Leave types/subtypes CRUD; leave request submit/list; request state transitions | Employee can submit requests; status updates correctly | Planned | Depends on Sprint 3 |
| Sprint 5 | Approvals and overrides | Manager approve/decline; HR override actions; approval timeline persistence | Manager path works; HR overrides are auditable | Planned | Depends on Sprint 4 |
| Sprint 6 | Attendance and edits | Clock in/out (single daily pair); attendance corrections with reason; attendance audit views | Unique daily attendance enforced; edits tracked before/after | Planned | Depends on Sprint 3 |
| Sprint 7 | Balance ledger and dashboards | Balance event ledger; employee summary dashboard; manager + HR dashboards | Balance calculations match event history; dashboard data validated by tests | Planned | Depends on Sprints 4-6 |
| Sprint 8 | Hardening and release candidate | End-to-end tests; API documentation finalization; runbook and migration notes | Critical scenarios pass; MVP checklist signed off | Planned | Final MVP gate |

## Status Legend
- `Planned`: defined but not started
- `In Progress`: currently being implemented
- `Blocked`: waiting on dependency/decision
- `Completed`: delivered and verified
