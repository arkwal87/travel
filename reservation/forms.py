from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy

from reservation.models import Room, Hotel, Client, Counterparty, ContractRoom, Contract, \
    Villa, ContractVilla


class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["first_name", "last_name", "date_of_birth", "phone_number", "email", "city", "postcode", "address",
                  "reference", "leader"]
        labels = {
            "first_name": "Imię",
            "last_name": "Nazwisko",
            "date_of_birth": "Data urodzenia",
            "phone_number": "Numer telefonu",
            "email": "Adres e-mail",
            "city": "Miasto",
            "postcode": "Kod pocztowy",
            "address": "Ulica",
            "reference": "Referencje",
            "leader": "Lider",
        }


class HotelCreateForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["region", "name", "link"]
        labels = {
            'name': 'Nazwa',
        }


class CounterpartyCreateForm(forms.ModelForm):
    class Meta:
        model = Counterparty
        fields = ["short_name", "full_name", "VAT_no", "country", "post_code", "city", "address"]
        labels = {
            "short_name": "Nazwa",
            "full_name": "Pełna nazwa",
            "VAT_no": "nr VAT",
            "country": "Kraj",
            "post_code": "Kod pocztowy",
            "city": "Miasto",
            "address": "Adres",
        }


class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        widgets = {"hotel": forms.HiddenInput}


class ContractRoomCreateForm(forms.ModelForm):
    class Meta:
        model = ContractRoom
        fields = "__all__"
        widgets = {'contract': forms.HiddenInput}


class ContractVillaCreateForm(forms.ModelForm):
    class Meta:
        model = ContractVilla
        fields = "__all__"
        widgets = {'contract': forms.HiddenInput}


class VillaCreateForm(forms.ModelForm):
    class Meta:
        model = Villa
        fields = ["region", "name", "size", "rooms_no", "pool", "link"]
        labels = {
            'name': 'Nazwa',
            'size': 'Powierzchnia [m2]',
            'rooms_no': 'Liczba pokoi',
            'pool': 'Basen'
        }
