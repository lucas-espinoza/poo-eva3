# Viajes Aventura

Aplicación web académica para administrar destinos, paquetes turísticos y reservas.

## Inicio rápido para evaluación

Requisito: tener **Python 3.10 o superior** instalado. Abra una terminal en esta carpeta y ejecute un único archivo:

```powershell
python iniciar_aplicacion.py
```

En el primer inicio, el programa instalará Django si es necesario, preparará la base de datos y pedirá los datos para crear el administrador. Elija y guarde su propio correo y contraseña: no hay credenciales predeterminadas.

Luego abra [http://127.0.0.1:8000/packages/](http://127.0.0.1:8000/packages/).

En los siguientes inicios, el programa conserva la base de datos y el administrador existente; solamente aplica migraciones pendientes y abre el servidor. Para detenerlo, vuelva a la terminal y presione `Ctrl+C`.

## Uso como administrador

1. Inicie sesión en [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/) con el correo y contraseña creados.
2. Abra **Destinos** y cree al menos dos destinos disponibles.
3. Abra **Paquetes**, seleccione **Nuevo paquete**, complete los datos, elija entre dos y cinco destinos y guarde el borrador.
4. Abra el paquete creado y pulse **Publicar**. Los clientes solo ven paquetes publicados, habilitados y con salida futura.
5. En **Reservas**, el administrador puede marcar solicitudes pendientes como pagadas o rechazadas.

También está disponible el panel estándar de Django en [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/), aunque la gestión cotidiana se realiza desde los accesos de la barra superior.

## Uso como cliente

1. Cree una cuenta en **Crear cuenta**. El RUT debe escribirse sin puntos, con guion y dígito verificador (por ejemplo, `12345678-5`).
2. Explore los paquetes publicados y seleccione **Ver experiencia**.
3. Pulse **Reservar ahora**, indique la cantidad de personas y confirme la solicitud.
4. Consulte **Mis reservas** para ver el estado. La reserva comienza como pendiente; el administrador confirma o rechaza su pago.

## Notas

- La información se guarda localmente en `db.sqlite3` y se conserva entre ejecuciones.
- Si Django no está instalado, el inicio requiere acceso a internet una sola vez para descargar las dependencias de `requirements.txt`.
- El proyecto está preparado para uso local de evaluación en `127.0.0.1`.
