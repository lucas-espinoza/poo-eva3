from datetime import timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from accounts.models import User
from destinations.models import Destination
from .models import Package
from .services import publish_package, save_draft


class PackageTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(email="staff@example.com", password="pass", first_name="S", last_name="T", rut="12345678-5", telephone="1", is_staff=True)
        self.a = Destination.objects.create(name="A", zone="N", description="a", duration_days=2, base_cost=100)
        self.b = Destination.objects.create(name="B", zone="S", description="b", duration_days=3, base_cost=200)
        today = timezone.localdate(); self.package = Package(name="Aventura", departure_date=today + timedelta(days=5), return_date=today + timedelta(days=8), maximum_capacity=5, margin=50)
    def test_composition_price_and_immutable_snapshots(self):
        save_draft(self.package, [self.a, self.b]); publish_package(self.package); self.package.refresh_from_db()
        self.assertEqual(self.package.published_price_per_person, 350)
        self.a.base_cost = 999; self.a.save(); self.package.refresh_from_db()
        self.assertEqual(self.package.published_price_per_person, 350)
        self.assertEqual(self.package.package_destinations.get(destination=self.a).base_cost_snapshot, 100)
        with self.assertRaises(ValidationError): save_draft(self.package, [self.a, self.b])
        self.package.margin = 999
        with self.assertRaises(ValidationError): self.package.save()
    def test_invalid_composition_rejected(self):
        with self.assertRaises(ValidationError): save_draft(self.package, [self.a])
        self.package.return_date = self.package.departure_date
        with self.assertRaises(ValidationError): self.package.full_clean()
    def test_destination_can_be_reused_between_drafts(self):
        save_draft(self.package, [self.a, self.b])
        today = timezone.localdate()
        another = Package(name="Otra", departure_date=today + timedelta(days=10), return_date=today + timedelta(days=12), maximum_capacity=2, margin=0)
        save_draft(another, [self.a, self.b])
        self.assertEqual(self.a.package_links.count(), 2)
    def test_catalog_has_friendly_empty_state(self):
        self.client.force_login(self.staff)
        response = self.client.get("/packages/")
        self.assertContains(response, "Pronto habrá nuevas aventuras")
