import uuid
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from packages.models import Package


class Reservation(models.Model):
    class PaymentState(models.TextChoices):
        PENDING = "pending", "Pendiente"
        PAID = "paid", "Pagado"
        REJECTED = "rejected", "Rechazado"
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reservations")
    package = models.ForeignKey(Package, on_delete=models.PROTECT, related_name="reservations")
    people_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    booked_price_per_person = models.PositiveIntegerField()
    total_charged = models.PositiveIntegerField()
    issued_at = models.DateTimeField(auto_now_add=True)
    submission_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    payment_state = models.CharField(max_length=10, choices=PaymentState.choices, default=PaymentState.PENDING)
    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(people_count__gt=0), name="reservation_positive_people")]
        ordering = ["-issued_at"]
