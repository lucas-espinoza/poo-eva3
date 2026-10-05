## Purpose

Maintain a reliable staff-managed catalog of travel destinations while preserving destinations that are part of historical package offers.

## Requirements

### Requirement: Staff manage valid destinations
The system SHALL let authorized staff create, view, edit, and list destinations with a unique name, zone, description, duration in days, and base per-person cost. Duration and base cost MUST be greater than zero. (R1, R2)

#### Scenario: Valid destination is created
- **WHEN** staff submit a destination with a new name, positive duration, and positive base cost
- **THEN** the system stores it as available for package creation

#### Scenario: Duplicate or non-positive destination data is rejected
- **WHEN** staff submit a duplicate name, zero/negative duration, or zero/negative base cost
- **THEN** the system rejects the submission and preserves the prior catalog state

### Requirement: Destination retirement preserves package history
The system SHALL allow an unused destination to be deleted. If a destination belongs to one or more packages, the system MUST retain it and mark it unavailable for new package composition instead. (R8)

#### Scenario: Unused destination is deleted
- **WHEN** staff delete a destination that belongs to no package
- **THEN** it is removed from the catalog

#### Scenario: Used destination is deactivated
- **WHEN** staff attempt to delete a destination that belongs to a package
- **THEN** the system retains it, marks it unavailable, and preserves existing package content
