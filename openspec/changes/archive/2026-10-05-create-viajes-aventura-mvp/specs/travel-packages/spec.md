## Purpose

Let authorized staff compose and publish dependable travel offers whose dates, capacity, content, and advertised price remain historically trustworthy.

## ADDED Requirements

### Requirement: Package composition supports valid destination reuse
The system SHALL let authorized staff create a package draft containing two through five distinct available destinations. A destination MAY be included in multiple packages. (R3, R4)

#### Scenario: Valid package composition is accepted
- **WHEN** staff select two to five different available destinations for a draft
- **THEN** the system saves the composition

#### Scenario: Invalid composition is rejected
- **WHEN** staff submit fewer than two, more than five, or repeated destinations in a package
- **THEN** the system rejects the composition

### Requirement: Package operating values are valid
The system SHALL require a package name, a return date later than its departure date, a maximum capacity greater than zero, and a non-negative operating margin. (R5, R6)

#### Scenario: Invalid dates, capacity, or margin are rejected
- **WHEN** staff submit a return date on/before departure, non-positive capacity, or negative margin
- **THEN** the system rejects publication and identifies the invalid field without changing a published offer

### Requirement: Publication fixes price and offer content
The system SHALL calculate a package's per-person price from the selected destinations' base costs plus the configured margin and SHALL fix the calculated price and applied destination-cost/content snapshot when the package is published. Later destination-cost changes MUST NOT alter a published package's price or historical composition. (R6, R7)

#### Scenario: Draft price is calculated for publication
- **WHEN** staff review a valid draft with selected destinations and a margin
- **THEN** the system shows the sum of current base costs and the resulting per-person price

#### Scenario: Published price survives catalog cost change
- **WHEN** staff publish a package and later change a constituent destination's base cost
- **THEN** the published package retains its original per-person price and applied composition snapshot

### Requirement: Only enabled current offers are customer-visible
The system SHALL expose only published, enabled packages with a future departure date to customer browsing. Drafts, disabled packages, and packages whose departure date has passed MUST remain unavailable for new customer reservations while historical records and existing reservations remain retained.

#### Scenario: Customer browses offers
- **WHEN** a customer views the package catalog
- **THEN** the catalog excludes drafts, disabled packages, and packages with a past departure date

#### Scenario: Employee disables a published package
- **WHEN** authorized staff mark a published future package as disabled
- **THEN** it is hidden from new customer bookings and its existing reservations remain preserved
