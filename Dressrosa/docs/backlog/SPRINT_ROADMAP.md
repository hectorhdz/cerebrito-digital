# Sprint Roadmap

## Sprint 0 - Planning Baseline (current)
- Deliverables:
  - Project plan
  - Architecture UML diagrams
  - ER diagram
  - Workflow sequence diagrams
  - Product backlog and sprint roadmap
- Verification:
  - Docs present and reviewed

## Sprint 1 - Project Bootstrap
- Deliverables:
  - FastAPI app skeleton
  - Config and dependency management
  - SQLAlchemy base models + Alembic init
  - Health endpoint and base layout page
- Verification:
  - App boots locally
  - Initial migration applies

## Sprint 2 - Auth and Roles
- Deliverables:
  - Login/logout (username/password)
  - Password hashing and session auth
  - API token/JWT auth
  - Role guards (`employee`, `manager`, `hr`, `admin`)
- Verification:
  - Protected endpoints enforce roles
  - Auth integration tests pass

## Sprint 3 - Users and Organization
- Deliverables:
  - User CRUD
  - Role assignment
  - Employee-manager mapping
- Verification:
  - Admin/HR can manage users
  - Manager relationships query correctly

## Sprint 4 - Leave Taxonomy and Requests
- Deliverables:
  - Leave types and subtypes CRUD
  - Leave request submission and listing
  - Request state transitions
- Verification:
  - Employee can submit requests
  - Request status updates correctly

## Sprint 5 - Approvals and Overrides
- Deliverables:
  - Manager approve/decline
  - HR override actions
  - Approval timeline persistence
- Verification:
  - Manager-only normal approval
  - HR override always auditable

## Sprint 6 - Attendance and Edits
- Deliverables:
  - Clock in/out (single daily pair)
  - Attendance corrections with reasons
  - Attendance audit log views
- Verification:
  - Unique daily attendance enforced
  - Edits are tracked with before/after values

## Sprint 7 - Balance Ledger and Dashboards
- Deliverables:
  - Balance event ledger engine
  - Employee summary dashboard
  - Manager + HR operational dashboards
- Verification:
  - Balance calculations match event history
  - Dashboard data validated by tests

## Sprint 8 - Hardening and MVP Release Candidate
- Deliverables:
  - End-to-end test suite for critical flows
  - API documentation finalization
  - Operational runbook and migration notes
- Verification:
  - Critical scenarios pass
  - MVP checklist signed off
