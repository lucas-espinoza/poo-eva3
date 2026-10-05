from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from .rut import validate_rut

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, password=None, **extra_fields):
        if not email: raise ValueError("Se requiere correo electrónico.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True); extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=12, unique=True, validators=[validate_rut])
    telephone = models.CharField(max_length=30)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "rut", "telephone"]
    objects = UserManager()
    def __str__(self): return self.email
