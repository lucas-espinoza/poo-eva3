## Why

La interfaz actual cumple los flujos funcionales, pero usa HTML sin estilo y no ofrece una experiencia clara ni agradable para clientes y personal. Un diseño coherente y adaptable facilitará descubrir viajes, completar reservas y administrar el catálogo.

## What Changes

- Incorporar una identidad visual responsiva de turismo de aventura en las plantillas Django existentes.
- Añadir una navegación, jerarquía visual, formularios, mensajes y acciones consistentes y accesibles.
- Rediseñar las vistas de catálogo, detalle, autenticación, administración y reservas sin modificar sus reglas de negocio, rutas ni datos.
- Incluir estados visuales para listas vacías, errores de formularios y ofertas no disponibles.

## Capabilities

### New Capabilities
- `friendly-ui-design`: Presentación visual responsiva y accesible para los flujos actuales de Viajes Aventura.

### Modified Capabilities

Ninguna.

## Impact

- Afecta las plantillas bajo `templates/` y agrega recursos CSS locales servidos por Django.
- No cambia modelos, migraciones, APIs, autenticación ni dependencias externas.
