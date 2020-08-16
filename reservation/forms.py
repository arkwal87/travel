from django import forms
from django.core.exceptions import ValidationError

from reservation.models import Room, Reservation, Hotel


class ReservationCreateForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ("price_service", "client")

