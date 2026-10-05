## Why

Viajes Aventura currently manages destinations, package offers, and reservations through disconnected manual records. This creates duplicate information, overselling risk, expired offers, exposure of client data, and loss of the price that was agreed when an offer or reservation was made.

The MVP centralizes these operations in a server-rendered Django application and establishes auditable, enforceable business rules before operational data begins to be recorded.

## What Changes

- Create the Django MVT foundation with SQLite, a custom email-based user model, session authentication, and role-based access for staff and clients.
- Add a staff-managed destination catalog with server-side validation, availability management, and dependency-safe retirement.
- Add draft and published travel packages composed of two to five destinations, with validated dates, capacity, margins, and immutable published price/composition snapshots.
- Add customer-facing enabled-package browsing and authenticated reservations with employee-managed payment states, historical charges, privacy controls, and concurrency-safe capacity accounting.
- Define integration and regression scenarios that trace the existing rules R1-R17, including authorization, historical pricing, privacy, and concurrent booking behavior.
- Keep the first release limited to HTML rendered by Django templates; payment automation, electronic invoicing, external integrations, email, mobile apps, reporting, REST APIs, and SPAs are out of scope.

## Capabilities

### New Capabilities

- `base-and-users`: Django project foundation, custom user accounts, registration, authentication, role authorization, and protection of credentials and sensitive client data (R9-R11, R17).
- `destination-catalog`: Staff management of destinations, validation of catalog data, availability, and deletion/deactivation behavior (R1, R2, R8).
- `travel-packages`: Drafting and publishing package offers, destination composition, capacities, dates, margins, and immutable published pricing/content (R3-R7).
- `customer-reservations`: Customer package visibility, private reservation history, historical charges, payment states, availability validation, and concurrency-safe capacity consumption (R11-R16).
- `business-rule-integration-tests`: End-to-end and regression coverage that proves R1-R17 across the above capabilities, including concurrent reservation attempts.

### Modified Capabilities

None; this repository has no existing OpenSpec capabilities.

## Impact

- Adds a Python/Django application organized into `accounts`, `destinations`, `packages`, and `reservations`, with Django templates, forms, ORM migrations, and `django.test` coverage.
- Uses SQLite, Django Authentication, CSRF protection, `DecimalField` for money, `DateField` for business dates, and Chilean time-zone configuration for audit timestamps.
- Requires a custom user model from the first migration and environment-based configuration for secrets and `DEBUG`.
- Establishes the agreed RUT format (no points, hyphen, check-digit validation, unique per client), integer CLP amounts, enabled/disabled package visibility, and employee-managed payment states; published-package edits, idempotency, and SQLite lock-retry policy remain implementation details.
