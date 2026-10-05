import uuid
from django import forms


class ReservationForm(forms.Form):
    people_count = forms.IntegerField(min_value=1, label="Cantidad de personas", widget=forms.NumberInput(attrs={"placeholder": "Ejemplo: 2", "min": 1}), help_text="Indica cuántas personas viajarán, incluido quien reserva.")
    submission_token = forms.UUIDField(widget=forms.HiddenInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound: self.initial["submission_token"] = uuid.uuid4()
