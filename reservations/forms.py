import uuid
from django import forms


class ReservationForm(forms.Form):
    people_count = forms.IntegerField(min_value=1, label="Personas")
    submission_token = forms.UUIDField(widget=forms.HiddenInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound: self.initial["submission_token"] = uuid.uuid4()
