from django import forms
from django.forms import ModelForm
from .models import Destination


class DestinationForm(ModelForm):
    class Meta:
        model = Destination
        fields = ["name", "zone", "description", "duration_days", "base_cost", "is_available"]
        labels = {
            "name": "Nombre del destino", "zone": "Zona o región", "description": "Descripción",
            "duration_days": "Duración (días)", "base_cost": "Costo base (CLP)", "is_available": "Disponible para nuevos paquetes",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ejemplo: San Pedro de Atacama"}),
            "zone": forms.TextInput(attrs={"placeholder": "Ejemplo: Región de Antofagasta"}),
            "description": forms.Textarea(attrs={"placeholder": "Describe las actividades, atractivos y condiciones del destino.", "rows": 4}),
            "duration_days": forms.NumberInput(attrs={"placeholder": "Ejemplo: 3", "min": 1}),
            "base_cost": forms.NumberInput(attrs={"placeholder": "Ejemplo: 150000", "min": 1}),
        }
