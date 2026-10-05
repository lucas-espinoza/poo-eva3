from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from .models import Destination


class DestinationTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(email="staff@example.com", password="pass", first_name="S", last_name="T", rut="12345678-5", telephone="1", is_staff=True)
    def test_staff_crud_and_positive_values(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse("destinations:create"), {"name": "Atacama", "zone": "Norte", "description": "Desierto", "duration_days": 3, "base_cost": 120000, "is_available": True})
        self.assertEqual(response.status_code, 302); self.assertTrue(Destination.objects.filter(name="Atacama").exists())
        bad = self.client.post(reverse("destinations:create"), {"name": "Bad", "zone": "X", "description": "X", "duration_days": 0, "base_cost": 0})
        self.assertEqual(bad.status_code, 200); self.assertFalse(Destination.objects.filter(name="Bad").exists())
    def test_unused_deleted_and_used_deactivated(self):
        self.client.force_login(self.staff); unused = Destination.objects.create(name="Sur", zone="S", description="x", duration_days=2, base_cost=1)
        self.client.post(reverse("destinations:remove", args=[unused.pk])); self.assertFalse(Destination.objects.filter(pk=unused.pk).exists())
        used = Destination.objects.create(name="Centro", zone="C", description="x", duration_days=2, base_cost=1)
        from packages.models import Package, PackageDestination
        from django.utils import timezone
        from datetime import timedelta
        package = Package.objects.create(name="Borrador", departure_date=timezone.localdate() + timedelta(days=2), return_date=timezone.localdate() + timedelta(days=3), maximum_capacity=2)
        PackageDestination.objects.create(package=package, destination=used)
        self.client.post(reverse("destinations:remove", args=[used.pk])); used.refresh_from_db()
        self.assertFalse(used.is_available)
