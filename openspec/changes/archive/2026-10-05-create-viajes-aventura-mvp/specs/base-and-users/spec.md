## Purpose

Provide distinct employee and client accounts with safe authentication, controlled access, and privacy-preserving handling of client identity data.

## ADDED Requirements

### Requirement: Client account registration and authentication
The system SHALL let a client register with name, unique email, RUT, telephone, and password, and SHALL authenticate clients using the email and password. Passwords MUST never be stored or displayed in their submitted form. A duplicate email MUST be rejected without disclosing sensitive submitted data. (R9, R10)

#### Scenario: Client registers with a unique email
- **WHEN** a visitor submits complete valid registration data using an unused email
- **THEN** the system creates a client account and allows that account to sign in

#### Scenario: Duplicate email is rejected safely
- **WHEN** a visitor submits registration data using an existing email
- **THEN** the system rejects the registration and does not expose the visitor's RUT or telephone in the response

### Requirement: Client RUT is validated and unique
The system SHALL accept a client RUT only in a no-points, hyphenated format with a valid check digit, and SHALL require its value to be unique before creating the client record. Invalid or duplicate RUT input MUST be rejected without echoing sensitive submitted data.

#### Scenario: Valid unique RUT is accepted
- **WHEN** a visitor submits a correctly formatted RUT with a valid check digit that is not registered
- **THEN** the system accepts it as part of client registration

#### Scenario: Invalid or duplicate RUT is rejected
- **WHEN** a visitor submits a RUT with an invalid check digit, wrong format, or a value registered to another client
- **THEN** the system rejects registration without creating a client record or displaying the RUT in the error

### Requirement: Role-based private-area access
The system SHALL allow authorized staff to access catalog, package, and reservation administration, and SHALL restrict clients to their own customer functions. Anonymous visitors MUST be required to authenticate before customer-private functions. (R11)

#### Scenario: Client cannot administer the catalog
- **WHEN** an authenticated client requests a destination or package administration function
- **THEN** the system denies access without modifying catalog data

#### Scenario: Anonymous visitor attempts a private function
- **WHEN** an anonymous visitor requests a reservation or reservation-history function
- **THEN** the system redirects to authentication or denies access and creates no reservation

### Requirement: Sensitive client data privacy
The system SHALL not display RUT or telephone in staff lists, client-visible lists, or validation/error messages. (R17)

#### Scenario: Staff lists customer-related records
- **WHEN** authorized staff view a reservation listing
- **THEN** RUT and telephone are absent from the displayed rows
