from django import forms
from .models import Package
from .services import validate_composition


class PackageForm(forms.ModelForm):
    destinations = forms.ModelMultipleChoiceField(queryset=None, label="Destinos incluidos", help_text="Selecciona entre 2 y 5 destinos disponibles.")
    class Meta:
        model = Package
        fields = ["name", "departure_date", "return_date", "maximum_capacity", "margin", "is_enabled", "destinations"]
        labels = {
            "name": "Nombre del paquete", "departure_date": "Fecha de salida", "return_date": "Fecha de regreso",
            "maximum_capacity": "Capacidad máxima (personas)", "margin": "Margen adicional (CLP)", "is_enabled": "Habilitado para publicar",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ejemplo: Aventura en el Norte Grande"}),
            "departure_date": forms.DateInput(attrs={"type": "date", "placeholder": "AAAA-MM-DD", "title": "Formato: año-mes-día, por ejemplo 2026-12-20"}),
            "return_date": forms.DateInput(attrs={"type": "date", "placeholder": "AAAA-MM-DD", "title": "Formato: año-mes-día, por ejemplo 2026-12-25"}),
            "maximum_capacity": forms.NumberInput(attrs={"placeholder": "Ejemplo: 20", "min": 1}),
            "margin": forms.NumberInput(attrs={"placeholder": "Ejemplo: 30000", "min": 0}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from destinations.models import Destination
        self.fields["destinations"].queryset = Destination.objects.filter(is_available=True)
        self.fields["departure_date"].help_text = "Formato: AAAA-MM-DD. Debe ser una fecha futura."
        self.fields["return_date"].help_text = "Formato: AAAA-MM-DD. Debe ser posterior a la salida."
        if self.instance.pk: self.initial["destinations"] = self.instance.destinations.all()
    def clean_destinations(self):
        destinations = self.cleaned_data["destinations"]
        validate_composition(destinations)
        return destinations
