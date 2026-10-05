import time
from datetime import date
from django.core.exceptions import ValidationError
from django.db import OperationalError, transaction
from django.db.models import Sum
from django.utils import timezone
from packages.models import Package
from .models import Reservation


def paid_people(package):
    return package.reservations.filter(payment_state=Reservation.PaymentState.PAID).aggregate(total=Sum("people_count"))["total"] or 0


def eligible(package):
    return package.status == Package.Status.PUBLISHED and package.is_enabled and package.departure_date > date.today()


@transaction.atomic
def create_reservation(*, client, package, people_count, token):
    package = Package.objects.get(pk=package.pk)
    if not eligible(package): raise ValidationError("El paquete no está disponible.")
    if people_count < 1: raise ValidationError("La cantidad debe ser positiva.")
    if paid_people(package) + people_count > package.maximum_capacity: raise ValidationError("No hay cupos suficientes.")
    reservation, created = Reservation.objects.get_or_create(submission_token=token, defaults={"client": client, "package": package, "people_count": people_count, "booked_price_per_person": package.published_price_per_person, "total_charged": package.published_price_per_person * people_count})
    if not created and reservation.client_id != client.id: raise ValidationError("Intento de reserva inválido.")
    return reservation, created


def transition_reservation(reservation, state, retries=3):
    if state not in {Reservation.PaymentState.PAID, Reservation.PaymentState.REJECTED}: raise ValidationError("Estado de pago inválido.")
    for attempt in range(retries):
        try:
            with transaction.atomic():
                reservation = Reservation.objects.select_related("package").get(pk=reservation.pk)
                if reservation.payment_state != Reservation.PaymentState.PENDING: raise ValidationError("La reserva ya fue procesada.")
                package = reservation.package
                # A write on the package serializes SQLite payment confirmations before capacity is read.
                Package.objects.filter(pk=package.pk).update(updated_at=timezone.now())
                package.refresh_from_db()
                if state == Reservation.PaymentState.PAID:
                    if not eligible(package) or paid_people(package) + reservation.people_count > package.maximum_capacity:
                        raise ValidationError("No hay cupos suficientes para confirmar el pago.")
                reservation.payment_state = state
                reservation.save(update_fields=["payment_state"])
                return reservation
        except OperationalError:
            if attempt == retries - 1: raise ValidationError("No se pudo procesar la reserva; inténtelo nuevamente.")
            time.sleep(0.05 * (attempt + 1))
