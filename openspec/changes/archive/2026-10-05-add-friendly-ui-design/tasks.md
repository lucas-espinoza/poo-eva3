## 1. Shared visual foundation

- [x] 1.1 Add a local responsive CSS design system with color, spacing, typography, controls, cards, badges, focus states, and mobile breakpoints; verify it loads through Django static files.
- [x] 1.2 Redesign the shared base template with accessible page structure, role-aware navigation, session actions, and message feedback; verify anonymous, customer, and staff navigation links render correctly.

## 2. Customer experience

- [x] 2.1 Restyle registration and login pages with approachable form layouts, field-level errors, and protected-data-safe feedback; verify account tests and form submissions continue to pass.
- [x] 2.2 Redesign package catalog and detail pages as responsive offer cards with clear pricing, availability, and reservation calls to action; verify published eligible package browsing remains unchanged.
- [x] 2.3 Restyle reservation submission, history, and detail pages with readable status indicators and friendly empty states; verify ownership and reservation workflow tests pass.

## 3. Staff experience

- [x] 3.1 Redesign destination list and edit forms with scannable records, availability status, and visually distinct destructive actions; verify staff-only destination CRUD behavior remains unchanged.
- [x] 3.2 Redesign package management list, draft form, and staff detail views while preserving publish and enablement controls; verify package publication and immutability tests pass.
- [x] 3.3 Redesign reservation administration with structured records and explicit pending, paid, and rejected status/actions; verify only staff can transition payment states.

## 4. Quality verification

- [x] 4.1 Add template-facing regression tests for shared navigation, friendly empty states, and CSRF-preserved mutations; verify `python manage.py test` passes.
- [x] 4.2 Review desktop and narrow viewport layouts for no horizontal overflow and keyboard-visible controls; verify `python manage.py check` and the full Django test suite pass.
