from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    labels = {
        "first_name": "Nombres", "last_name": "Apellidos", "email": "Correo electrónico",
        "rut": "RUT", "telephone": "Teléfono", "password1": "Contraseña", "password2": "Confirmar contraseña",
    }
    placeholders = {
        "first_name": "Ejemplo: Camila", "last_name": "Ejemplo: González", "email": "Ejemplo: camila@correo.cl",
        "rut": "Ejemplo: 12345678-5", "telephone": "Ejemplo: +56 9 1234 5678",
        "password1": "Mínimo 8 caracteres", "password2": "Escribe nuevamente tu contraseña",
    }
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "rut", "telephone", "password1", "password2")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, label in self.labels.items():
            self.fields[name].label = label
            self.fields[name].widget.attrs["placeholder"] = self.placeholders[name]
        self.fields["rut"].help_text = "Sin puntos, con guion y dígito verificador."
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists(): raise forms.ValidationError("El correo ya está registrado.")
        return email
    def clean_rut(self):
        rut = self.cleaned_data["rut"].upper()
        if User.objects.filter(rut=rut).exists(): raise forms.ValidationError("El RUT ya está registrado.")
        return rut

class EmailAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Correo electrónico"
        self.fields["username"].widget.attrs["placeholder"] = "Ejemplo: nombre@correo.cl"
        self.fields["password"].label = "Contraseña"
        self.fields["password"].widget.attrs["placeholder"] = "Escribe tu contraseña"
    username = forms.EmailField(label="Correo electrónico")
