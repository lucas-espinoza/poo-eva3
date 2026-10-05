## Context

The project is a local Django/SQLite academic MVP with `requirements.txt` and `manage.py`, but it currently requires several commands to install dependencies, migrate the database, create a superuser, and start the server. See proposal.md for motivation and the guided-local-delivery specification for externally visible behavior.

## Goals / Non-Goals

**Goals:**

- Give evaluators a one-file startup path that is safe to repeat.
- Retain Django's interactive `createsuperuser` prompts so passwords are never embedded or logged by custom code.
- Document the concrete staff and customer workflow against the current UI.

**Non-Goals:**

- Package Python, provision a virtual environment, reset existing data, seed demonstration data, or deploy beyond localhost.
- Change application behavior or replace Django's administrator bootstrap.

## Decisions

### Root Python launcher with subprocess commands

Add a root-level Python launcher that resolves paths relative to itself and invokes the current interpreter for dependency, migration, superuser, and development-server commands. Using the current interpreter avoids platform-specific shell syntax and lets the professor run one `.py` file. A batch/PowerShell launcher was rejected because the requested artifact is portable Python.

### Check dependencies before installation

The launcher will first test whether Django is importable. If it is not, it will install the pinned project requirements through the current interpreter. It will display the action and propagate failures rather than hiding them. This avoids unnecessary package installation on repeat use while supporting a clean Python environment.

### Preserve existing administrator accounts

After migrations, the launcher will query the custom user model through Django to determine whether a superuser exists. Only a database with no superuser invokes `createsuperuser`; otherwise the script continues to the server. This makes reruns safe and preserves evaluator-created credentials.

### Documentation as an evaluator path

Write README in Spanish with prerequisites, one execution command, localhost URL, first-run behavior, staff workflow, customer workflow, and stop instructions. It will explain that data persists in SQLite and no default credentials exist, avoiding an unsafe shared password.

## Risks / Trade-offs

- [The evaluator lacks internet access and Django is not installed] → show an explicit dependency-installation failure and leave the database untouched.
- [A startup script could overwrite an evaluation database] → never delete or recreate SQLite data; run normal migrations only.
- [The server process blocks the terminal] → document that this is expected and can be stopped with Ctrl+C.
- [An existing user is not an administrator] → check specifically for a superuser, not merely any account.

## Migration Plan

1. Add the launcher and README without modifying the existing database schema.
2. Test a first-run path against a fresh SQLite database and a repeat path with an existing superuser.
3. Roll back by deleting only the launcher and README; application data remains unchanged.
