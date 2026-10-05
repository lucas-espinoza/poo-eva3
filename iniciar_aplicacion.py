"""Prepara Viajes Aventura y ejecuta el servidor local para evaluación."""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

if os.name == "nt":
    os.system("")  # Enables ANSI colors in supported Windows consoles.

PROJECT_DIR = Path(__file__).resolve().parent
MANAGE_PY = PROJECT_DIR / "manage.py"
REQUIREMENTS = PROJECT_DIR / "requirements.txt"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


def status(message: str, color: str = GREEN) -> None:
    print(f"{color}[OK] {message}{RESET}")


def run_command(arguments: list[str], *, quiet: bool = True) -> None:
    kwargs = {"cwd": PROJECT_DIR, "check": True}
    if quiet:
        kwargs.update({"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL})
    subprocess.run(arguments, **kwargs)


def ensure_python() -> None:
    if sys.version_info < (3, 10):
        raise RuntimeError("Se requiere Python 3.10 o superior para ejecutar la aplicación.")


def ensure_dependencies() -> None:
    if importlib.util.find_spec("django") is not None:
        status("Dependencias verificadas.")
        return
    print("Instalando dependencias del proyecto...")
    run_command([sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS)])
    status("Dependencias instaladas.")


def migrate_database() -> None:
    print("Preparando la base de datos...")
    run_command([sys.executable, str(MANAGE_PY), "migrate", "--noinput"])
    status("Base de datos migrada correctamente.")


def has_superuser() -> bool:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    import django

    django.setup()
    from django.contrib.auth import get_user_model

    return get_user_model().objects.filter(is_superuser=True).exists()


def bootstrap_administrator() -> None:
    if has_superuser():
        status("Administrador existente detectado.")
        return
    print("\nCree el administrador con los datos solicitados:")
    run_command([sys.executable, str(MANAGE_PY), "createsuperuser"], quiet=False)
    status("Administrador creado correctamente.")


def start_server() -> None:
    status("Aplicación lista: http://127.0.0.1:8000/packages/")
    print("Presione Ctrl+C para detener el servidor.")
    run_command([sys.executable, str(MANAGE_PY), "runserver", "127.0.0.1:8000"])


def main() -> int:
    try:
        ensure_python()
        ensure_dependencies()
        migrate_database()
        bootstrap_administrator()
        start_server()
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"\n{RED}[ERROR] No fue posible preparar la aplicación: {error}{RESET}", file=sys.stderr)
        return error.returncode if isinstance(error, subprocess.CalledProcessError) else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
