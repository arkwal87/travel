from django import forms
from django.core.exceptions import ValidationError

from reservation.models import Room, Reservation


class ReservationCreateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"
        widgets = {
            "client": forms.SelectMultiple
        }