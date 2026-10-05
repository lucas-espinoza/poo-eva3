## 1. Project foundation and accounts

- [x] 1.1 Create the Django project configuration, SQLite database settings, Chile time zone, environment-based `SECRET_KEY`/`DEBUG`, and four application modules; verify Django system checks pass.
- [x] 1.2 Implement and migrate the custom email-login user model before any dependent migrations, including unique email and unique validated RUT fields; verify migrations apply to a new SQLite database.
- [x] 1.3 Implement RUT format/check-digit validation for no-points, hyphenated input and register/login/logout forms using Django password hashing; verify model/form tests accept valid RUTs and reject malformed, invalid-check-digit, duplicate-email, and duplicate-RUT submissions.
- [x] 1.4 Configure staff and customer authorization boundaries, protected routes, base templates, CSRF-protected forms, and privacy-safe error rendering; verify anonymous and customer access-denial view tests pass.
- [x] 1.5 Add account privacy tests ensuring passwords, RUTs, and telephones are absent from list pages, validation messages, and logs rendered by the application.

## 2. Destination catalog

- [x] 2.1 Create destination migration/model with unique name, zone, description, positive duration/base-cost constraints, availability, and audit timestamps; verify migration and model constraint tests pass.
- [x] 2.2 Implement staff-only destination list, create, edit, and availability forms/views/templates; verify authorized CRUD tests and client-denial tests pass.
- [x] 2.3 Implement dependency-aware destination removal that deletes unused destinations and deactivates destinations referenced by packages; verify R8 unit and integration tests preserve package history.

## 3. Package drafts and publication

- [x] 3.1 Create package and package-destination migrations/models with draft/published status, enabled flag, date/capacity/margin checks, unique package-destination membership, and publication snapshots; verify migration and constraint tests pass.
- [x] 3.2 Implement staff-only draft creation/editing with selection of two through five distinct available destinations and reusable destinations across packages; verify valid and invalid composition tests pass.
- [x] 3.3 Implement server-side package price preview using integer CLP values and positive date/capacity/non-negative-margin validation; verify price-calculation and rejection tests pass.
- [x] 3.4 Implement transactional publication that fixes per-person price and component cost/content snapshots and prevents material mutation of published offers; verify destination-cost changes do not alter published prices or snapshots.
- [x] 3.5 Implement staff package list/detail and enabled/disabled control, plus customer catalog filtering for published, enabled, future offers; verify disabled, draft, and past packages cannot be browsed or newly reserved while existing records remain available to staff/history.

## 4. Reservations and payment states

- [x] 4.1 Create reservation migration/model with client/package links, people count, booked price/total snapshots, issuance timestamp, submission token, and `pending`/`paid`/`rejected` payment state; verify migrations and model tests pass.
- [x] 4.2 Implement authenticated customer package detail and reservation submission that validates positive people count, enabled future package status, capacity against paid reservations, and creates a pending historical reservation without consuming capacity; verify service and view tests pass.
- [x] 4.3 Implement private customer reservation history/detail queries constrained to the authenticated owner; verify manipulated-ID, anonymous, and cross-client privacy tests pass.
- [x] 4.4 Implement staff-only reservation administration with pending-to-paid and pending-to-rejected transitions, treating employee cancellation as rejection; verify only staff can change state and rejected/cancelled pending reservations consume no capacity.
- [x] 4.5 Implement transactional paid-capacity calculation and SQLite contention handling with bounded retries/controlled failure; verify concurrent payment-confirmation tests never commit paid people beyond package capacity.
- [x] 4.6 Implement duplicate-submission protection with a one-time reservation attempt token without blocking intentionally distinct bookings; verify repeated POST tests create at most one reservation per token.

## 5. Regression coverage and delivery verification

- [x] 5.1 Add a traceability matrix in the test suite mapping R1-R17 to model, service, and view tests; verify every rule identifier is represented by an automated scenario.
- [x] 5.2 Add end-to-end staff/customer workflow tests covering destination retirement, package publication snapshots, enabled visibility, private history, historical totals, and payment-state capacity behavior; verify the complete Django test suite passes.
- [x] 5.3 Add security regression tests for CSRF-protected mutations, password hashing, authorization, sensitive-data masking, and immutable published/charged values; verify all security tests pass.
- [x] 5.4 Run migrations against an empty SQLite database and the complete automated suite, including concurrent payment-confirmation coverage; verify no test leaves capacity above its maximum or exposes RUT/telephone data.
