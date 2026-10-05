from django.forms import ModelForm
from .models import Destination


class DestinationForm(ModelForm):
    class Meta:
        model = Destination
        fields = ["name", "zone", "description", "duration_days", "base_cost", "is_available"]
