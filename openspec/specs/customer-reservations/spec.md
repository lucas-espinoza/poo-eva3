## Purpose

Enable authenticated clients to reserve available published package seats safely, privately, and with an immutable record of the agreed charge.

## Requirements

### Requirement: Clients reserve only eligible packages
The system SHALL allow an authenticated client to create a pending reservation for one or more people on an enabled published package only when its departure date has not passed and requested people count is at least one and no greater than capacity remaining after paid reservations. Pending reservations MUST NOT consume capacity. (R11, R14, R15, R16)

#### Scenario: Valid pending reservation does not consume capacity
- **WHEN** an authenticated client reserves a positive number of people within capacity remaining after paid reservations of a future enabled published package
- **THEN** the system creates a pending reservation and does not reduce capacity

#### Scenario: Invalid reservation is rejected
- **WHEN** a client requests zero people, more people than capacity remaining after paid reservations, or a disabled/past-departure package
- **THEN** the system rejects the request and does not consume capacity

### Requirement: Reservation charges are historical
The system SHALL record the reservation issue time, client, package, people count, package per-person price at booking, and total charged. Total charged MUST equal the fixed package price multiplied by people count at booking and MUST NOT be recalculated after creation. (R12, R13)

#### Scenario: Booking total remains unchanged
- **WHEN** a reservation is created and a later change affects package or destination pricing
- **THEN** its recorded per-person price and total charged remain unchanged

### Requirement: Reservation history is private
The system SHALL allow clients to view only their own reservation history and MUST deny access to another client's reservation even if its identifier is manipulated. (R11)

#### Scenario: Client requests another client's reservation
- **WHEN** a client requests a reservation owned by another client
- **THEN** the system denies access and does not disclose reservation details

### Requirement: Employee-managed payment state controls capacity
The system SHALL create reservations in `pending` payment state. Only authorized employees SHALL change a reservation to `paid` or `rejected`. A transition to `paid` MUST be accepted only when the reservation's people count fits within capacity remaining after other paid reservations; paid reservations consume capacity. Rejecting a pending payment, or employee cancellation implemented as transition to `rejected`, MUST leave or release capacity. (R14)

#### Scenario: Employee marks pending payment as paid
- **WHEN** authorized staff mark a pending reservation as paid and sufficient capacity remains
- **THEN** the system records it as paid and consumes its people count from availability

#### Scenario: Employee rejects or cancels pending payment
- **WHEN** authorized staff reject or cancel a pending reservation
- **THEN** the system records it as rejected and no capacity is consumed

### Requirement: Concurrent payment confirmation never oversells capacity
The system SHALL ensure simultaneous payment confirmations cannot create paid reservations whose combined people count exceeds package maximum capacity. If contention cannot be completed, the system MUST return a controlled failure without recording an over-capacity payment confirmation. (R14)

#### Scenario: Concurrent confirmations exceed last seats
- **WHEN** concurrent pending-reservation payment confirmations together request more than the remaining capacity
- **THEN** only confirmations fitting within capacity succeed and the total people in paid reservations never exceeds maximum capacity
