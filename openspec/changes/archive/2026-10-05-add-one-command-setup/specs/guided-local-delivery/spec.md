## Purpose

Permitir que un evaluador inicie y use la entrega local de Viajes Aventura con un único archivo Python y una guía en español, sin conocer comandos internos del proyecto.

## ADDED Requirements

### Requirement: Single-command local startup
The project SHALL provide a root-level Python startup script that a local evaluator can execute to prepare the application and start the local development server without manually running Django management commands.

#### Scenario: First-time evaluator starts the project
- **WHEN** an evaluator executes the startup script from a checkout with Python and network access for missing dependencies
- **THEN** the script installs declared dependencies if needed, applies database migrations, guides administrator creation, and starts the local server

### Requirement: Administrator bootstrap is safe and guided
The startup flow SHALL detect whether an administrator account already exists. It MUST prompt for Django's administrator details only when no administrator exists and MUST not create a duplicate administrator automatically.

#### Scenario: Existing administrator is detected
- **WHEN** an evaluator executes the startup script after an administrator was already created
- **THEN** the script reports that the existing administrator can be used and starts the server without prompting for another account

### Requirement: Clear startup failure feedback
The startup script SHALL report a clear next step and terminate with a nonzero result when Python requirements, dependency installation, migrations, or administrator bootstrap fail.

#### Scenario: Dependency installation fails
- **WHEN** required dependencies are missing and cannot be installed
- **THEN** the script reports the failed preparation step and does not start a partially prepared server

### Requirement: Evaluator usage guide
The project SHALL include a Spanish `README.md` that states the single startup command, the browser address, how to access staff administration, how to create and publish a package, how a client reserves it, and how to stop the server.

#### Scenario: Evaluator follows the manual
- **WHEN** an evaluator reads the README before running the project
- **THEN** the evaluator can start the application and complete the primary administrator and customer flows without consulting source code
