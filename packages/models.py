from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from destinations.models import Destination


class Package(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Borrador"
        PUBLISHED = "published", "Publicado"
    name = models.CharField(max_length=160)
    departure_date = models.DateField()
    return_date = models.DateField()
    maximum_capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    margin = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    is_enabled = models.BooleanField(default=True)
    published_price_per_person = models.PositiveIntegerField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destinations = models.ManyToManyField(Destination, through="PackageDestination", related_name="packages")
    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(maximum_capacity__gt=0), name="package_positive_capacity"), models.CheckConstraint(condition=models.Q(margin__gte=0), name="package_nonnegative_margin")]
    def clean(self):
        if self.departure_date and self.return_date and self.return_date <= self.departure_date:
            raise ValidationError({"return_date": "La fecha de regreso debe ser posterior a la salida."})
    def save(self, *args, **kwargs):
        if self.pk:
            previous = type(self).objects.filter(pk=self.pk).values("status", "name", "departure_date", "return_date", "maximum_capacity", "margin", "published_price_per_person").first()
            protected = ("name", "departure_date", "return_date", "maximum_capacity", "margin", "published_price_per_person")
            if previous and previous["status"] == self.Status.PUBLISHED and any(previous[field] != getattr(self, field) for field in protected):
                raise ValidationError("Los valores materiales de un paquete publicado son inmutables.")
        return super().save(*args, **kwargs)
    @property
    def current_price(self):
        return sum(link.destination.base_cost for link in self.package_destinations.select_related("destination")) + self.margin
    def __str__(self): return self.name


class PackageDestination(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="package_destinations")
    destination = models.ForeignKey(Destination, on_delete=models.PROTECT, related_name="package_links")
    base_cost_snapshot = models.PositiveIntegerField(null=True, blank=True)
    name_snapshot = models.CharField(max_length=120, blank=True)
    description_snapshot = models.TextField(blank=True)
    duration_days_snapshot = models.PositiveIntegerField(null=True, blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["package", "destination"], name="unique_package_destination")]
