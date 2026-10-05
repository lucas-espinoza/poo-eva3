## Context

The current server-rendered Django views use minimal semantic HTML in shared and feature-specific templates. The application already has functional URL, authorization, CSRF, and validation behavior that must remain unchanged. See proposal.md for motivation and the friendly-ui-design spec for observable behavior.

## Goals / Non-Goals

**Goals:**

- Establish reusable visual tokens and components through one local stylesheet and the shared base template.
- Make customer and staff workflows clear on mobile and desktop using the existing template context.
- Preserve accessible semantic controls, focus visibility, contrast, and server-rendered feedback.

**Non-Goals:**

- Changing application workflows, permissions, domain models, URLs, or form field semantics.
- Adding a JavaScript framework, external UI library, image assets, or remote font dependency.
- Replacing the Django administration site.

## Decisions

### Local CSS design system

Add a single static stylesheet using CSS custom properties for color, spacing, typography, controls, cards, badges, and responsive breakpoints. A local stylesheet keeps the academic project self-contained and avoids availability, privacy, and version risk from a CDN. A component framework was not selected because it would add a dependency and require adapting existing server-rendered markup.

### Shared layout and role-aware navigation

Extend the base template with the application header, navigation links appropriate to anonymous users, customers, and staff, a constrained main content area, and accessible message markup. Feature templates will use shared utility/component classes. This centralizes consistency rather than duplicating navigation and styling on every page.

### Enhance existing templates without changing contracts

Refactor only template markup and classes around existing variables, forms, and URL names. Keep each POST form, CSRF token, action URL, and server-rendered error behavior intact. This avoids an accidental change to authorization or booking behavior while improving presentation.

### Responsive content patterns

Use flexible grids for catalog cards, action groups that wrap, and scrollable table/list containers where structured staff data needs multiple columns. Small screens collapse navigation and multi-column content without removing any workflow action.

## Risks / Trade-offs

- [A visual rewrite could omit a mutation control or CSRF token] → preserve form structures and run the complete Django suite after template changes.
- [Color-only status indicators may not be accessible] → pair colors with explicit text and visible labels.
- [Staff records can be dense on mobile] → use responsive cards or horizontally contained tables while retaining all permitted actions.
- [Static files might not load in production configuration] → use Django static template tags and validate with the development server and test suite.

## Migration Plan

1. Add the local static stylesheet and reference it from the shared layout.
2. Upgrade base, account, destination, package, and reservation templates incrementally.
3. Run template-facing and full regression tests on desktop and narrow viewport checks.
4. Roll back by reverting only template and static-file changes; no data migration is required.
