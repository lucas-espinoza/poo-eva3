from django.core.validators import MinValueValidator
from django.db import models


class Destination(models.Model):
    name = models.CharField(max_length=120, unique=True)
    zone = models.CharField(max_length=120)
    description = models.TextField()
    duration_days = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    base_cost = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(duration_days__gt=0), name="destination_positive_duration"), models.CheckConstraint(condition=models.Q(base_cost__gt=0), name="destination_positive_cost")]
        ordering = ["name"]

    def __str__(self): return self.name
