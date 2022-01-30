from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy

from reservation.models import Room, Hotel, Client, Counterparty, ContractRoom, Contract, \
    Villa, ContractVilla, ContractTrain, ContractInsurance, ContractTicket, ContractOther

LABELS = {
    "first_name": "Imię",
    "last_name": "Nazwisko",
    "date_of_birth": "Data urodzenia",
    "phone_number": "Numer telefonu",
    "email": "Adres e-mail",
    "city": "Miasto",
    "postcode": "Kod pocztowy",
    "address": "Ulica",
    "reference": "Referencje",
    "short_name": "Nazwa",
    "full_name": "Pełna nazwa",
    "VAT_no": "nr VAT",
    "country": "Kraj",
    "post_code": "Kod pocztowy",
    "villa": "Villa",
    "room": "Pokój",
    "date_from": "Od",
    "date_to": "Do",
    "room_number": "Liczba pokoii",
    "price_offer": "Cena offer",
    "price_net": "Cena net",
    "offer_currency": "Waluta offer",
    "net_currency": "Waluta net",
    "counterparty": "Kontrahent",
    "meal_plan": "Wyżywienie",
    "category": "Kategoria",
    "name": "Nazwa",
    "hotel": "Hotel",
    "room_size": "Powierzchnia pokoju [m2]",
    "terrace_size": "Powierzchnia tarasu [m2]",
    "train": "Nazwa pociągu",
    "cabin_category": "Kategoria kabiny",
    "type": "Typ ubezpieczenia",
    "ticket": "Trasa",
    "ticket_class": "Klasa",
    "airline": "Linia lotniczna",
    "date_departure": "Odlot",
    "date_arrival": "Przylot",
    "extra_notes": "Dodatkowe informacje",
    "description": "Opis",
    'size': 'Powierzchnia [m2]',
    'rooms_no': 'Liczba pokoi',
}


class DateInput(forms.DateInput):
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["first_name", "last_name", "date_of_birth", "phone_number", "email", "city", "postcode", "address",
                  "reference"]
        labels = LABELS


class HotelCreateForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["region", "name", "link", "category"]
        labels = LABELS


class CounterpartyCreateForm(forms.ModelForm):
    class Meta:
        model = Counterparty
        fields = ["short_name", "full_name", "VAT_no", "country", "post_code", "city", "address"]
        labels = LABELS


class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        labels = LABELS
        widgets = {"hotel": forms.HiddenInput}


class ContractRoomCreateForm(forms.ModelForm):
    class Meta:
        model = ContractRoom
        fields = "__all__"
        labels = LABELS
        widgets = {
            'contract': forms.HiddenInput,
            'date_from': DateInput(),
            'date_to': DateInput(),
        }


class ContractVillaCreateForm(forms.ModelForm):
    class Meta:
        model = ContractVilla
        fields = "__all__"
        labels = LABELS
        widgets = {
            'contract': forms.HiddenInput,
            'date_from': DateInput(),
            'date_to': DateInput(),
        }


class ContractTrainCreateForm(forms.ModelForm):
    class Meta:
        model = ContractTrain
        fields = "__all__"
        labels = LABELS
        widgets = {
            'contract': forms.HiddenInput,
            'date_from': DateInput(),
            'date_to': DateInput(),
        }


class ContractInsuranceCreateForm(forms.ModelForm):
    class Meta:
        model = ContractInsurance
        fields = "__all__"
        labels = LABELS
        widgets = {'contract': forms.HiddenInput}


class ContractTicketCreateForm(forms.ModelForm):
    class Meta:
        model = ContractTicket
        fields = "__all__"
        labels = LABELS
        widgets = {
            'contract': forms.HiddenInput,
            'date_departure': DateTimeInput(),
            'date_arrival': DateTimeInput()
        }


class ContractOtherCreateForm(forms.ModelForm):
    class Meta:
        model = ContractOther
        fields = "__all__"
        labels = LABELS
        widgets = {'contract': forms.HiddenInput}


class VillaCreateForm(forms.ModelForm):
    class Meta:
        model = Villa
        fields = ["region", "name", "size", "rooms_no", "link"]
        labels = LABELS
