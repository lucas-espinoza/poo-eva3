# Viajes Aventura — especificación inicial para OpenSpec

## 1. Objetivo del proyecto

Construir una aplicación web para la agencia **Viajes Aventura**, que arma y vende paquetes turísticos propios combinando destinos del catálogo. La primera versión debe sustituir la planilla de destinos y paquetes, el cuaderno de reservas y las consultas manuales, evitando duplicaciones, sobreventa, fechas vencidas y alteraciones de precios históricos.

Este documento es la **fuente inicial de requisitos para OpenSpec**, no una implementación. Distinguir las reglas vigentes del caso de los supuestos propuestos que deben confirmarse.

## 2. Tecnologías y arquitectura obligatorias

- **Lenguaje:** Python.
- **Framework:** Django con arquitectura **MVT (Model–View–Template)** y renderizado HTML desde el servidor.
- **Base de datos:** SQLite y migraciones con Django ORM.
- **Paradigma:** programación orientada a objetos (modelos, formularios, clases de servicio donde agreguen valor y pruebas).
- **Autenticación:** Django Authentication con sesiones, contraseñas protegidas mediante los hashers del framework y control de permisos para empleados y clientes.
- **Interfaz:** Django Templates y formularios Django con protección CSRF. No crear API REST ni frontend SPA en la primera versión sin necesidad demostrada.
- **Dinero:** `DecimalField`, nunca `float` para cálculos monetarios.
- **Fechas:** fechas del negocio con `DateField`, zona horaria de Chile para los tiempos de auditoría y registro.
- **Organización:** módulos Django separados por responsabilidades (`accounts`, `destinations`, `packages`, `reservations`) sin capas ni patrones adicionales innecesarios.

## 3. Actores y acceso

### Administrador / empleado
- Inicio y cierre de sesión.
- Alta, edición, desactivación y consulta de destinos.
- Creación y administración de paquetes, fechas, márgenes, cupos y publicación.
- Consulta de reservas y disponibilidad.
- Acceso exclusivamente autorizado a los datos de clientes.
- Se consideran inicialmente los tres socios como personal autorizado, sin asumir nuevos puestos.

### Cliente
- Registro con nombre, RUT, correo electrónico, teléfono y contraseña.
- Inicio y cierre de sesión.
- Consulta de paquetes publicados y disponibilidad.
- Creación de reservas propias y consulta de su historial y estado.
- No puede ver ni modificar reservas de otros clientes.

## 4. Modelo funcional y reglas de negocio vigentes

La siguiente enumeración corresponde a las **reglas R1–R17 del documento del caso**. Implementarlas como validaciones de servidor y cubrirlas con pruebas.

### Destinos
- **R1.** Un destino tiene nombre, zona, descripción, duración en días y costo base por persona. El nombre es único en el catálogo.
- **R2.** El costo base de un destino debe ser mayor que cero.
- **R8.** Un destino que no pertenece a ningún paquete se puede eliminar. Si pertenece a alguno, se marca como **no disponible** y deja de ofrecerse para nuevos paquetes; los paquetes ya vendidos conservan su contenido.

### Paquetes
- **R3.** Un paquete combina entre **dos y cinco** destinos, sin destinos repetidos dentro del mismo paquete.
- **R4.** Un destino puede formar parte de múltiples paquetes simultáneamente.
- **R5.** Cada paquete tiene nombre, fecha de salida, fecha de regreso y cupo máximo. La fecha de regreso es posterior a la de salida y el cupo es mayor que cero.
- **R6.** El administrador define las fechas y el margen de operación (habitualmente 20 %, nunca negativo). El precio por persona se calcula sumando los costos base de los destinos incluidos y agregando ese margen: `precio = suma_costos * (1 + margen / 100)`.
- **R7.** El precio queda **fijado cuando el paquete se publica**. Los cambios posteriores en costos de destinos no cambian los precios de paquetes ya publicados.

### Clientes y seguridad
- **R9.** Un cliente se registra con nombre, RUT, correo electrónico, teléfono y contraseña. El correo lo identifica y no se repite.
- **R10.** La contraseña nunca se almacena tal como fue escrita: utilizar el hashing nativo de Django.
- **R11.** Solo un cliente autenticado puede reservar y consultar reservas, y únicamente las suyas.
- **R17.** RUT y teléfono son datos sensibles: no deben mostrarse en listados ni mensajes de error.

### Reservas
- **R12.** Una reserva corresponde a un cliente y un paquete. Registra fecha de emisión, cantidad de personas y total cobrado.
- **R13.** Al reservar se calcula `total = precio_por_persona_del_paquete * personas`, y ese total permanece inmutable.
- **R14.** `cupo_disponible = cupo_maximo - personas_ya_reservadas`. No se acepta una reserva cuya cantidad supere el cupo disponible.
- **R15.** No se acepta una reserva si la fecha de salida del paquete ya pasó.
- **R16.** La cantidad de personas reservadas debe ser al menos una.

## 5. Proceso de creación y publicación de paquetes

1. Un empleado autenticado crea o mantiene destinos con nombre único, zona, descripción, duración y costo base por persona mayor que cero.
2. Crea un **borrador** de paquete e indica nombre comercial, salida, regreso y cupo máximo.
3. Selecciona entre 2 y 5 destinos disponibles, sin repetir ninguno; los mismos destinos pueden aparecer en otros paquetes.
4. Indica margen porcentual no negativo (valor sugerido inicial: 20 %).
5. El sistema calcula en el servidor la suma de costos por persona y el precio resultante; muestra un resumen antes de publicar.
6. Al publicar, valida todas las reglas y fija el precio por persona y la composición del paquete. No debe depender de costos actualizados para reconstruir lo vendido.
7. Los clientes ven únicamente paquetes publicados y vigentes con cupos disponibles según las decisiones de visibilidad indicadas en la sección de supuestos.
8. Al reservar, se guarda el precio total vigente en ese instante, no un cálculo dinámico sobre los costos del catálogo.

**Ejemplo documental:** paquete "Norte Grande en 5 días" combina Salar de Surire ($310.000) y Valle del Elqui ($120.000). Suma base $430.000; con margen 20 %, el precio por persona sería **$516.000**. El margen de este ejemplo es una aplicación del margen habitual, no un precio publicado que figure expresamente en el caso.

## 6. Modelo de datos propuesto (Django ORM)

### Usuario
- Preferir un **Custom User Model** desde la primera migración, con correo único como identificador de inicio de sesión.
- Nombre, correo, RUT, teléfono y contraseña gestionada por Django.
- `is_staff`, `is_active`, permisos y grupos nativos de Django.
- No mostrar RUT ni teléfono en listados y excepciones.
- No almacenar contraseñas en texto plano, ni incluirlas en logs.

### Destino (`Destination`)
- `id`, `name` (único), `zone`, `description`, `duration_days`, `base_cost`, `is_available`, `created_at`, `updated_at`.
- Validación `duration_days > 0` y `base_cost > 0`.
- Proteger dependencias históricas para cumplir R8.

### Paquete (`Package`)
- `id`, `name`, `departure_date`, `return_date`, `max_capacity`, `margin_percent`, `status` (borrador/publicado; otros estados solo si se aprueban), `published_price_per_person` (nulo hasta publicación), `published_at`, `created_at`.
- Relación entre paquete y destinos mediante modelo intermedio `PackageDestination` con unicidad compuesta `package + destination`.
- Conservar una instantánea de la composición/costos aplicados a la publicación mediante el modelo intermedio (`base_cost_snapshot`) u otro mecanismo explícito e inmutable.
- Validar cantidad de destinos, fechas, margen y cupo en una operación de publicación transaccional.

### Reserva (`Reservation`)
- `id`, `client` (FK a usuario), `package` (FK), `created_at`, `people_count`, `total_charged`, `price_per_person_snapshot`.
- El **total cobrado** debe ser un dato histórico conservado, no una propiedad que se recalcule desde el paquete.
- Si se agrega `status` para necesidades administrativas, sus estados y efectos en el cupo deben acordarse expresamente (ver supuestos).

## 7. Operaciones y pantallas mínimas

### Empleados
- Acceso al área privada.
- Listado, creación, modificación y desactivación de destinos.
- Creación de borradores, selección de destinos, cálculo de precio y publicación de paquetes.
- Listado de paquetes con precios, fechas, cupos y disponibilidad.
- Listado/consulta de reservas con controles de privacidad.

### Clientes
- Registro e inicio de sesión.
- Listado de paquetes publicados (precios, fechas, destinos y disponibilidad).
- Detalle del paquete y formulario para reservar cupos.
- Confirmación y consulta de historial de **reservas propias**.

## 8. Integridad, concurrencia y seguridad

- Validar siempre del lado del servidor; no confiar en formularios ni en valores enviados por el navegador.
- Usar `transaction.atomic()` para publicación y reservas.
- **Evitar sobreventa bajo concurrencia real.** En SQLite, `select_for_update()` no ofrece bloqueos de fila efectivos: no utilizarlo como única defensa. Para la reserva, diseñar una sección de escritura serializada/condicionada, usar transacciones adecuadas y gestionar `database is locked` con una política limitada de reintentos o respuesta controlada. Añadir prueba concurrente para que nunca se exceda el cupo.
- Limitar edición de paquetes publicados cuando afecte precios, fechas, destinos o cupos ya vendidos. No sobrescribir la historia.
- Usar permisos Django, decoradores/mixins de acceso, protección CSRF, validación de objetos pertenecientes al usuario y plantillas con escape predeterminado.
- Usar restricciones de base de datos (`UniqueConstraint`, `CheckConstraint`) donde sean aplicables; las reglas interrelacionales necesitan validación de dominio transaccional.
- Configurar secretos y `DEBUG` mediante variables de entorno; no subir la base de datos con información real al repositorio.

## 9. Dentro y fuera del alcance

### Incluido en primera versión
- Destinos: registrar, modificar, marcar no disponible y listar.
- Paquetes: crear combinando destinos, definir fechas y cupos, calcular precios, publicar y consultar disponibilidad.
- Clientes: registro, autenticación, reserva e historial propio.
- Seguridad: autenticación, validación de datos y protección de credenciales y datos sensibles.
- Acceso de empleados para administrar el catálogo y paquetes.

### Excluido en primera versión
- Pasarela de pagos y verificación automática de transferencias.
- Facturación electrónica ante el SII.
- Aplicación para teléfonos móviles.
- Integraciones con aerolíneas, hoteles o operadores externos.
- Envío de mensajes o correos a clientes.
- Informes de gestión, contabilidad o remuneraciones.

**Importante:** el caso indica que los clientes pagan mediante transferencia verificada manualmente, pero el primer alcance **no incluye** una pasarela ni verificación automática. No inferir que exista cobro electrónico, conciliación bancaria ni confirmación automática de pago.

## 10. Vacíos del caso y supuestos propuestos (NO son reglas vigentes)

El documento solicita detectar y resolver estos vacíos, fundamentando cada decisión en diseño. No presentar las siguientes sugerencias como decisiones ya aprobadas:

1. **Eliminación de reservas:** propuesta: no habilitar cancelación ni eliminación en el MVP hasta definir su efecto en el cupo y trazabilidad.
2. **Fin de temporada / visibilidad:** propuesta: no mostrar paquetes cuya salida ya pasó y conservarlos con sus reservas en el historial. Definir explícitamente cómo se despublican paquetes sin borrar información histórica.
3. **Quién modifica:** propuesta: solo usuarios `is_staff` autorizados administran destinos y paquetes; clientes solo actúan sobre sus reservas.
4. **Edición tras publicación:** propuesta: los campos determinantes del precio o del contenido publicado son inmutables; crear una nueva oferta ante cambios materiales.
5. **Cupos y reservas:** propuesta: toda reserva creada consume cupo de inmediato; no hay vencimientos automáticos ni estados de pago en el MVP, salvo acuerdo expreso.
6. **Duplicados:** propuesta: cada envío válido produce una reserva, pero prevenir reenvíos accidentales mediante token único/idempotente por intento; no prohibir automáticamente reservas distintas del mismo cliente al mismo paquete sin una regla expresa.
7. **RUT:** definir su formato, normalización, validación de dígito verificador y unicidad. El documento solo exige que sea registrado y protegido, no afirma explícitamente que deba ser único.
8. **Cálculo de moneda:** proponer CLP con montos enteros y redondeo comercial explícito al peso en la publicación; el documento no define política de redondeo.
9. **Costo histórico de destinos:** guardar instantánea al publicar es una decisión de implementación para satisfacer R7 y R8.
10. **Capacidad SQLite:** adecuada para un proyecto de escala pequeña y uso académico; verificar concurrencia en pruebas y considerar PostgreSQL si más adelante aumenta la carga de escrituras.

## 11. Criterios de aceptación y pruebas

- Impide crear destinos con nombres duplicados o costos no positivos.
- No elimina físicamente un destino que forma parte de paquetes, pero permite desactivarlo.
- Rechaza paquetes de 0, 1 o más de 5 destinos, y destinos repetidos.
- Acepta la reutilización de un destino entre varios paquetes.
- Rechaza regreso anterior o igual a salida, cupo no positivo y margen negativo.
- Calcula precio como suma de costos por persona más margen.
- Cambiar el costo de un destino no altera el precio ya publicado.
- Rechaza reservas de menos de una persona, con cupo insuficiente o con salida pasada.
- No excede cupo ni ante solicitudes concurrentes.
- Las reservas almacenan y conservan el total calculado al momento de reservar.
- No se puede consultar el historial de otro cliente por manipulación de URL/ID.
- No permite al usuario anónimo reservar, ni al cliente administrar el catálogo.
- El correo del cliente es único y las contraseñas se almacenan con hash.
- RUT y teléfono no aparecen en listados ni mensajes de error.
- Implementar tests de modelos, servicios y vistas con `django.test`.

## 12. Orden sugerido de implementación mediante OpenSpec

Solicitar que OpenSpec genere propuestas, especificaciones verificables, diseño y tareas **antes de crear código**, separando por capacidades:

1. **Base y usuarios:** proyecto Django, SQLite, custom user, registro, autenticación, permisos, layouts y pruebas.
2. **Catálogo:** destinos, validaciones, disponibilidad y restricciones de eliminación.
3. **Paquetes:** composición, fechas, márgenes, publicación y precio inmutable.
4. **Reservas:** disponibilidad, privacidad, total histórico y control concurrente.
5. **Pruebas de integración:** escenarios y regresiones de R1–R17.

No introducir Django REST Framework, Celery, microservicios, Docker obligatorio ni frontend JavaScript independiente sin requerimiento concreto.

## 13. Instrucción inicial para el agente OpenSpec

> Lee íntegramente `INICIO_OPENSPEC_VIAJES_AVENTURA.md` y usa las secciones 1–9 y 11 como requisitos de partida para crear una propuesta OpenSpec de la primera versión de Viajes Aventura. Conserva el identificador de las reglas R1–R17 y deriva escenarios comprobables por regla. Trata la sección 10 como supuestos pendientes de aprobación, no como reglas confirmadas; señala las decisiones que condicionen el modelo y la funcionalidad. Produce propuesta, diseño, especificaciones y tareas en incrementos pequeños según la sección 12. Utiliza Python, Django MVT, SQLite, Django Authentication, HTML renderizado y programación orientada a objetos. Antes de implementar, revisa integridad, sobreventa, privacidad y conservación de precios históricos. No escribas código todavía.

---

**Referencia de origen:** documento escaneado «Caso: Agencia de Viajes — Viajes Aventura», apartados 1–6 y reglas vigentes R1–R17. El caso identifica expresamente vacíos que deben resolverse mediante decisiones fundamentadas; dichas decisiones aparecen diferenciadas en la sección 10.
