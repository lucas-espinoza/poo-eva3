## Context

This is a greenfield academic MVP. The required behavior is defined by the change specs and the rationale is in [proposal.md](proposal.md). The application must use Python, Django MVT, server-rendered HTML, SQLite, Django authentication, and the four bounded Django apps `accounts`, `destinations`, `packages`, and `reservations`.

The principal technical constraints are preserving published and booked monetary history, enforcing rules R1-R17 server-side, avoiding sensitive-data exposure, and preventing overselling despite SQLite's limited write concurrency. Business dates are calendar dates; audit timestamps use the Chile time zone.

## Goals / Non-Goals

**Goals:**

- Make domain invariants enforceable at the database, form, and transactional service boundaries.
- Preserve package price/content and reservation charges as historical facts.
- Keep browser interactions conventional, protected server-rendered form submissions.
- Provide a testable, small-module design with explicit authorization boundaries.

**Non-Goals:**

- Building REST endpoints, a SPA, automatic payment verification, messaging, external integrations, accounting, or operational reporting.
- Designing for high-volume multi-node writes; SQLite is retained for the academic MVP.
- Inferring policy decisions omitted by the case as confirmed requirements.
- Use docker.

## Decisions

### Django MVT modules and authorization boundaries

Use a custom email-login user model from the first migration in `accounts`; retain Django's password hashing, session authentication, groups/permissions, `is_staff`, CSRF middleware, and template autoescaping. Staff-only views use server-side authorization mixins/decorators; customer reservation queries are always constrained to the current authenticated user.

This uses framework features already required by the project and keeps authorization adjacent to each view. A separate API/auth service was considered and rejected because it adds interfaces and attack surface outside the MVP.

### Domain data and constraint layers

`Destination` holds catalog data and availability. `Package` has draft/published state, an enabled flag, date/capacity/margin values, and nullable published price/time. `PackageDestination` is the association table, uniquely keyed by package/destination, and records an immutable base-cost snapshot at publication. `Reservation` records owner, package, timestamp, people count, booked per-person price, immutable total, and payment state.

Use database uniqueness/check constraints where a row-local rule can be represented (email, RUT, destination name, positive values, unique association). Validate RUT's no-points/hyphenated format and check digit before persistence. Use Django forms/model validation for user feedback, and domain services inside transactions for cross-row invariants: two-to-five destinations, publication, and remaining capacity. Database constraints alone cannot express these aggregate/stateful rules; forms alone are bypassable.

### Price representation and historical snapshots

All monetary fields use fixed-precision decimal values; calculations execute on the server. Publication copies component costs and fixes `published_price_per_person`; booking copies that price and fixes `total_charged`. Customer-facing and staff historical views read snapshots, never a live destination-cost calculation.

This prevents R7/R13 regressions and supports R8 history. Storing only formulas/live references was rejected because catalog edits would retroactively change what was offered or charged.

Use integer CLP amounts for display and stored package/reservation monetary values. The server fixes the calculated amount to whole pesos at publication.

### Publication, enablement, and post-publication changes

Publish through one transactional domain operation that revalidates staff input, availability, composition, dates, capacity, and non-negative margin immediately before fixing the snapshot and status. Published packages have an employee-managed enabled/disabled flag: disabled offers are hidden and cannot receive new reservations, while existing reservations remain retained. Treat package fields that determine content, price, dates, or capacity as immutable after publication; material amendments create a new draft offer. Past-departure packages are withheld from new customer browsing/reservations but retained for history.

This preserves an audit trail. Allowing in-place changes was rejected because it produces ambiguous historical commitments.

### Reservation payment lifecycle, capacity, and SQLite contention

Reservation creation records a historical price/total and starts in `pending`, but does not consume capacity. Only authorized employees can transition a pending reservation to `paid` or `rejected`; a cancellation is recorded as `rejected`. Payment confirmation uses a single transactional service that validates enabled/future package eligibility and availability calculated from paid reservations, then commits the state transition. Paid reservations consume capacity; rejecting or cancelling a pending payment consumes none. Because SQLite lacks reliable row-level `select_for_update()` semantics, it MUST NOT be the sole capacity defense. Serialize the critical payment-confirmation write path using SQLite-appropriate transaction acquisition/conditional write behavior, convert lock contention into a bounded retry, and return a controlled retry/error result once the retry budget is exhausted. A concurrent test must prove paid reservations never exceed capacity.

This favors correctness over maximum write throughput. A naive read-then-insert flow and row locking alone were rejected because concurrent writers can overbook on SQLite. If expected write contention grows, migrate the same domain contract to PostgreSQL with database-supported row locking or equivalent conditional updates.

### Reservation submission and duplicate prevention

For the MVP, successfully created reservations remain retained in `pending`, `paid`, or `rejected` state. There is no deletion, expiration, automatic payment verification, or automatic reconciliation. Use a one-time server-generated submission token for a reservation attempt to reduce accidental browser re-posts without forbidding deliberately separate bookings by the same client.

This preserves the manual-transfer boundary of the MVP while making capacity depend only on employee-confirmed payments.

### RUT handling

Store RUT as protected profile data in the validated no-points, hyphenated format and never include it in list projections, validation responses, or logs. Validate its check digit before persistence and enforce a uniqueness constraint. Keep validation/normalization behind a dedicated form/domain boundary.

This protects client identity data while ensuring one account per registered RUT. Generic free-text storage was rejected because it allows malformed or duplicate identifiers.

## Risks / Trade-offs

- [SQLite permits only limited concurrent writing and can report `database is locked`] → Keep reservation writes short, use a bounded retry/controlled failure policy, and test concurrent booking; plan PostgreSQL when workload requires it.
- [Aggregate rules can be bypassed outside forms] → Revalidate them in transactional domain services and cover model/service/view paths with tests.
- [Payment confirmation and package enablement change availability after a customer has created a pending reservation] → Revalidate eligibility and paid capacity transactionally at every employee state transition.
- [Published data needs correction] → Preserve the immutable offer and create a replacement draft rather than rewriting history.

## Migration Plan

1. Configure the custom user model and base settings before the first migration.
2. Add app migrations in dependency order: accounts, destinations, packages and snapshots, then reservations and constraints.
3. Seed only non-sensitive development data; configure secrets and `DEBUG` through environment variables.
4. Run automated unit, view, and concurrency tests before accepting operational data.
5. Roll back a failed pre-production deployment by restoring the previous database backup and application release; do not manually delete historical package/reservation rows to undo a migration.
