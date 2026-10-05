## Why

La entrega académica necesita poder ser evaluada sin que el profesor deba conocer comandos de Django ni configurar manualmente la base de datos. También requiere una guía breve y precisa para operar los flujos principales del sistema.

## What Changes

- Agregar un único script Python de inicio que compruebe requisitos, instale dependencias declaradas cuando falten, ejecute migraciones, solicite crear el primer administrador y levante el servidor local.
- Hacer que el flujo no duplique administradores: si ya existe uno, informará al evaluador y continuará con el servidor.
- Añadir un `README.md` en español que explique el inicio mediante ese script, el acceso y los flujos de administrador y cliente.

## Capabilities

### New Capabilities
- `guided-local-delivery`: Inicio autónomo de la aplicación local y documentación de uso para evaluación académica.

### Modified Capabilities

Ninguna.

## Impact

- Agrega un script Python de raíz y un manual `README.md`.
- Usa `requirements.txt`, `manage.py`, SQLite y el servidor de desarrollo ya existentes.
- No cambia modelos, migraciones, rutas, permisos ni reglas de negocio.
