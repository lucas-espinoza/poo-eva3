from django import forms
from .models import Package
from .services import validate_composition


class PackageForm(forms.ModelForm):
    destinations = forms.ModelMultipleChoiceField(queryset=None)
    class Meta:
        model = Package
        fields = ["name", "departure_date", "return_date", "maximum_capacity", "margin", "is_enabled", "destinations"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from destinations.models import Destination
        self.fields["destinations"].queryset = Destination.objects.filter(is_available=True)
        if self.instance.pk: self.initial["destinations"] = self.instance.destinations.all()
    def clean_destinations(self):
        destinations = self.cleaned_data["destinations"]
        validate_composition(destinations)
        return destinations
