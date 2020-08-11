from django import forms
from django.core.exceptions import ValidationError

from reservation.models import Hotel


class HotelCreateForm(forms.ModelForm):
    class Meta:
        model = Hotel