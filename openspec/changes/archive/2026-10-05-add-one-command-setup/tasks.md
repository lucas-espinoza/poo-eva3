## 1. Guided startup launcher

- [x] 1.1 Create a root-level Python launcher that resolves the project directory, verifies Python compatibility, and installs `requirements.txt` only when Django is unavailable; verify a mocked missing-dependency path invokes the current interpreter's pip command.
- [x] 1.2 Add migration execution and failure handling to the launcher; verify it runs `manage.py migrate --noinput` before any database query and exits clearly when preparation fails.
- [x] 1.3 Add safe superuser detection and interactive bootstrap using Django's existing command; verify a fresh SQLite database prompts for a superuser and a subsequent run skips the prompt.
- [x] 1.4 Start Django's local development server on `127.0.0.1:8000` after successful preparation; verify the launcher displays the URL and propagates Ctrl+C/server exit normally.

## 2. Evaluator documentation

- [x] 2.1 Write a Spanish `README.md` with prerequisites, the one-command startup instruction, initial administrator creation, browser URL, persisted-data note, and stop instruction; verify it can be followed without invoking Django commands directly.
- [x] 2.2 Document the staff workflow for destinations, package publication, and payment administration, plus the customer registration/reservation workflow; verify every documented URL and action matches the current application.

## 3. Regression verification

- [x] 3.1 Add automated tests for launcher command sequencing and repeat-safe administrator detection; verify `python manage.py test` passes.
- [x] 3.2 Run the launcher preparation flow against a fresh SQLite database without destructive changes to existing data, then run `python manage.py check` and the full test suite.
