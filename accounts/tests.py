from django.test import Client, TestCase
from django.urls import reverse
from unittest.mock import patch
import iniciar_aplicacion
from .forms import RegistrationForm
from .models import User
from .rut import validate_rut


class AccountTests(TestCase):
    def registration_data(self, **overrides):
        data = {"first_name": "Ana", "last_name": "Pérez", "email": "ana@example.com", "rut": "12345678-5", "telephone": "999999999", "password1": "correct-horse-123", "password2": "correct-horse-123"}
        data.update(overrides); return data
    def test_rut_validation_and_safe_registration(self):
        form = RegistrationForm(self.registration_data()); self.assertTrue(form.is_valid()); user = form.save()
        self.assertTrue(user.check_password("correct-horse-123"))
        self.assertFalse(RegistrationForm(self.registration_data(email="other@example.com", rut="12345678-4")).is_valid())
        response = self.client.post(reverse("accounts:register"), self.registration_data(email="ana@example.com", rut="11111111-1", telephone="888"))
        self.assertNotContains(response, "11111111-1"); self.assertNotContains(response, "888")
    def test_private_routes_and_staff_boundary(self):
        response = self.client.get(reverse("reservations:history")); self.assertEqual(response.status_code, 302)
        client = User.objects.create_user(email="client@example.com", password="pass", first_name="C", last_name="L", rut="11111111-1", telephone="7")
        self.client.force_login(client)
        self.assertEqual(self.client.get(reverse("destinations:list")).status_code, 302)
    def test_mutating_form_requires_csrf(self):
        secure_client = Client(enforce_csrf_checks=True)
        response = secure_client.post(reverse("accounts:register"), self.registration_data())
        self.assertEqual(response.status_code, 403)
    def test_navigation_shows_role_appropriate_links(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertContains(response, "Crear cuenta")
        staff = User.objects.create_user(email="staff@example.com", password="pass", first_name="S", last_name="T", rut="12345678-5", telephone="1", is_staff=True)
        self.client.force_login(staff)
        response = self.client.get(reverse("packages:catalog"))
        self.assertContains(response, "Destinos")
        self.assertContains(response, "Reservas")


class LauncherTests(TestCase):
    def test_missing_django_installs_with_current_interpreter(self):
        with patch("iniciar_aplicacion.importlib.util.find_spec", return_value=None), patch("iniciar_aplicacion.run_command") as command:
            iniciar_aplicacion.ensure_dependencies()
        command.assert_called_once_with([iniciar_aplicacion.sys.executable, "-m", "pip", "install", "-r", str(iniciar_aplicacion.REQUIREMENTS)])

    def test_prepare_order_migrates_before_superuser_check(self):
        with patch("iniciar_aplicacion.ensure_python"), patch("iniciar_aplicacion.ensure_dependencies"), patch("iniciar_aplicacion.migrate_database") as migrate, patch("iniciar_aplicacion.bootstrap_administrator") as bootstrap, patch("iniciar_aplicacion.start_server"):
            self.assertEqual(iniciar_aplicacion.main(), 0)
        migrate.assert_called_once()
        bootstrap.assert_called_once()

    def test_existing_administrator_skips_creation(self):
        with patch("iniciar_aplicacion.has_superuser", return_value=True), patch("iniciar_aplicacion.run_command") as command:
            iniciar_aplicacion.bootstrap_administrator()
        command.assert_not_called()
