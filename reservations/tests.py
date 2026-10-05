import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, TransactionTestCase
from django.db import close_old_connections
from django.db.models import Sum
from django.utils import timezone
from accounts.models import User
from destinations.models import Destination
from packages.models import Package
from packages.services import publish_package, save_draft
from .models import Reservation
from .services import create_reservation, transition_reservation


class ReservationTests(TestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(email="client@example.com", password="pass", first_name="C", last_name="U", rut="12345678-5", telephone="1")
        self.other = User.objects.create_user(email="other@example.com", password="pass", first_name="O", last_name="U", rut="11111111-1", telephone="2")
        today = timezone.localdate(); self.package = Package.objects.create(name="P", departure_date=today + timedelta(days=3), return_date=today + timedelta(days=5), maximum_capacity=3, margin=0)
        a = Destination.objects.create(name="A", zone="N", description="a", duration_days=1, base_cost=100); b = Destination.objects.create(name="B", zone="S", description="b", duration_days=1, base_cost=100)
        save_draft(self.package, [a, b]); publish_package(self.package); self.package.refresh_from_db()
    def test_pending_is_idempotent_historical_and_private(self):
        token = uuid.uuid4(); reservation, created = create_reservation(client=self.client_user, package=self.package, people_count=2, token=token)
        same, created_again = create_reservation(client=self.client_user, package=self.package, people_count=2, token=token)
        self.assertTrue(created); self.assertFalse(created_again); self.assertEqual(reservation.total_charged, 400)
        self.client.force_login(self.other); self.assertEqual(self.client.get(f"/reservations/{reservation.pk}/").status_code, 404)
    def test_paid_capacity_and_rejection(self):
        first, _ = create_reservation(client=self.client_user, package=self.package, people_count=2, token=uuid.uuid4())
        second, _ = create_reservation(client=self.other, package=self.package, people_count=2, token=uuid.uuid4())
        transition_reservation(first, Reservation.PaymentState.PAID); self.assertEqual(Reservation.objects.get(pk=first.pk).payment_state, Reservation.PaymentState.PAID)
        with self.assertRaises(ValidationError): transition_reservation(second, Reservation.PaymentState.PAID)
        self.assertEqual(Reservation.objects.get(pk=second.pk).payment_state, Reservation.PaymentState.PENDING)


class ConcurrentCapacityTests(TransactionTestCase):
    def test_simultaneous_confirmations_never_exceed_capacity(self):
        one = User.objects.create_user(email="one@example.com", password="pass", first_name="O", last_name="N", rut="12345678-5", telephone="1")
        two = User.objects.create_user(email="two@example.com", password="pass", first_name="T", last_name="W", rut="11111111-1", telephone="2")
        today = timezone.localdate()
        package = Package.objects.create(name="Concurrente", departure_date=today + timedelta(days=3), return_date=today + timedelta(days=5), maximum_capacity=3, margin=0)
        a = Destination.objects.create(name="CA", zone="N", description="a", duration_days=1, base_cost=100)
        b = Destination.objects.create(name="CB", zone="S", description="b", duration_days=1, base_cost=100)
        save_draft(package, [a, b]); publish_package(package)
        first, _ = create_reservation(client=one, package=package, people_count=2, token=uuid.uuid4())
        second, _ = create_reservation(client=two, package=package, people_count=2, token=uuid.uuid4())
        barrier = Barrier(2)
        def confirm(pk):
            close_old_connections(); barrier.wait()
            try: transition_reservation(Reservation.objects.get(pk=pk), Reservation.PaymentState.PAID)
            except ValidationError: pass
            finally: close_old_connections()
        with ThreadPoolExecutor(max_workers=2) as workers:
            list(workers.map(confirm, [first.pk, second.pk]))
        paid = Reservation.objects.filter(package=package, payment_state=Reservation.PaymentState.PAID).aggregate(total=Sum("people_count"))["total"] or 0
        self.assertLessEqual(paid, package.maximum_capacity)
