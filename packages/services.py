from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from .models import Package, PackageDestination


def validate_composition(destinations):
    ids = list(destinations.values_list("id", flat=True)) if hasattr(destinations, "values_list") else [d.id for d in destinations]
    if not 2 <= len(ids) <= 5:
        raise ValidationError("Un paquete requiere entre dos y cinco destinos.")
    if len(ids) != len(set(ids)):
        raise ValidationError("Los destinos deben ser distintos.")


@transaction.atomic
def save_draft(package, destinations):
    if package.status == Package.Status.PUBLISHED:
        raise ValidationError("Un paquete publicado no puede modificarse.")
    validate_composition(destinations)
    if any(not destination.is_available for destination in destinations):
        raise ValidationError("Solo se pueden usar destinos disponibles.")
    package.full_clean(); package.save()
    package.package_destinations.all().delete()
    PackageDestination.objects.bulk_create([PackageDestination(package=package, destination=d) for d in destinations])
    return package


@transaction.atomic
def publish_package(package):
    package = Package.objects.select_for_update().get(pk=package.pk)
    if package.status == Package.Status.PUBLISHED:
        raise ValidationError("El paquete ya fue publicado.")
    links = list(package.package_destinations.select_related("destination"))
    validate_composition([link.destination for link in links])
    if any(not link.destination.is_available for link in links):
        raise ValidationError("Hay destinos no disponibles.")
    package.full_clean()
    price = sum(link.destination.base_cost for link in links) + package.margin
    for link in links:
        d = link.destination
        link.base_cost_snapshot, link.name_snapshot, link.description_snapshot, link.duration_days_snapshot = d.base_cost, d.name, d.description, d.duration_days
    PackageDestination.objects.bulk_update(links, ["base_cost_snapshot", "name_snapshot", "description_snapshot", "duration_days_snapshot"])
    package.published_price_per_person, package.status, package.published_at = price, Package.Status.PUBLISHED, timezone.now()
    package.save()
    return package
