# Dressrosa Project Plan

## 1. Product Goal
Dressrosa is a single-company HR web application to manage:
- Employee daily work status (remote/office)
- Attendance clock-in/clock-out (one pair per day)
- Leave request lifecycle
- Manager approvals and HR super-approval overrides
- Leave balance visibility and reporting

## 2. Scope (MVP)
### Included
- Username/password authentication
- Role-based authorization: `employee`, `manager`, `hr`, `admin`
- Leave types + scalable subtypes
- Leave request submission, approval/decline, and override handling
- One daily clock-in and one daily clock-out
- Authorized attendance corrections with audit trail
- REST API v1 for all core resources
- Server-rendered web UI (Jinja2 + HTMX)

### Excluded (Post-MVP)
- Multi-company/tenant support
- External SSO providers
- Mobile app
- Complex scheduling or shift planning

## 3. Technical Stack
- Backend: FastAPI (Python)
- Frontend: Jinja2 templates + HTMX
- Database: SQLite (migration-ready for PostgreSQL)
- ORM/Data: SQLAlchemy + Alembic
- Auth: Password hash + session for web + token for API
- Testing: Pytest

## 4. Architecture Style
- Modular monolith
- Clear separation:
  - Web routes (`/web/*`)
  - REST API (`/api/v1/*`)
  - Domain services
  - Persistence layer
- API-first contracts to enable future separate clients

## 5. Core Domain Modules
- Auth & Access Control
- Users & Organization
- Attendance
- Leave Management
- Approvals
- Audit & Reporting

## 6. Data and Policy Principles
- Leave taxonomy is configuration-driven (`type` + `subtype` tables)
- Balance is computed from ledger-like events:
  - Accrual
  - Reservation (on request submit, if applicable)
  - Consumption (on approval/date reached)
  - Reversal (on decline/cancel)
- Every approval and attendance correction is auditable

## 7. Non-Functional Requirements (Initial)
- Traceability: all critical actions logged
- Consistency: transactional updates for approval and balance movements
- Simplicity: SQLite-first, migration path for PostgreSQL
- Maintainability: explicit module boundaries and testable services

## 8. Delivery Strategy
- Small, verifiable increments by sprint
- Each sprint produces testable behavior + updated docs
- Keep API contracts stable through `/api/v1`

## 9. Definition of Done (Per Sprint)
- Feature works in both web flow and API where applicable
- Role checks enforced
- Basic automated tests added/updated
- Docs and backlog updated
