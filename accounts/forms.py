from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "rut", "telephone", "password1", "password2")
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists(): raise forms.ValidationError("El correo ya está registrado.")
        return email
    def clean_rut(self):
        rut = self.cleaned_data["rut"].upper()
        if User.objects.filter(rut=rut).exists(): raise forms.ValidationError("El RUT ya está registrado.")
        return rut

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Correo electrónico")
