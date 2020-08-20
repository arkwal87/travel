from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy

from reservation.models import Room, Reservation, Hotel, RoomReservation


class ReservationCreateForm(forms.ModelForm):

    def clean(self):
        clean_data = super().clean()
        if clean_data["price_service"] < 0:
            raise ValidationError("Cena serwisu nie może być mniejsza niż 0")
        return clean_data

    class Meta:
        model = Reservation
        fields = ("owner", "price_service", "client")


class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        widgets = {"hotel": forms.HiddenInput}


class RoomReservationCreateForm(forms.ModelForm):
    class Meta:
        model = RoomReservation
        fields = "__all__"