from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy

from reservation.models import Room, Hotel, Client, Counterparty, ContractRoom, Contract, \
    Villa, ContractVilla, ContractTrain, ContractInsurance, ContractTicket, ContractOther, ContractFile, Payment

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
    "cabin_name": "Nazwa kabiny",
    "type": "Typ ubezpieczenia",
    "ticket": "Trasa",
    "ticket_class": "Klasa",
    "airline": "Linia lotniczna",
    "date_departure": "Odlot",
    "date_arrival": "Przylot",
    "extra_notes": "Dodatkowe informacje",
    "description": "Opis",
    "size": "Powierzchnia [m2]",
    "rooms_no": "Liczba pokoi",
    "date_of_sign": "Data podpisania",
    "client": "Lista klientów",
    "owner": "Właściciel",
    "leader": "Lider",
    "payment_deadline": "Data płatności",
    "cancellation_deadline": "Data anulowania",
    "cancellation_policy": "Polityka rezygnacji",
    "payment_policy": "Polityka płatności",
    "quantity": "Ilość",
    "payment_date": "Data wpłaty",
    "value": "Wartość",
    "currency": "Waluta",
    "ticket_details": "Szczegóły biletu"
}


class DateInput(forms.DateInput):
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class ContractCreateForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = "__all__"
        widgets = {
            "date_of_contract": forms.HiddenInput,
            "name": forms.HiddenInput,
            "date_of_sign": DateInput(),
            "cancellation_deadline": DateInput(),
            "payment_deadline": DateInput()
        }
        labels = LABELS


class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["first_name", "last_name", "date_of_birth", "phone_number", "email", "city", "postcode", "address",
                  "reference"]
        widgets = {"date_of_birth": DateInput()}
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

    def clean_date_to(self):
        date_to = self.cleaned_data.get('date_to')
        date_from = self.cleaned_data.get('date_from')
        if date_to < date_from:
            raise forms.ValidationError('Sprawdź poprawność dat')


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

    def clean_date_to(self):
        date_to = self.cleaned_data.get('date_to')
        date_from = self.cleaned_data.get('date_from')
        if date_to < date_from:
            raise forms.ValidationError('Sprawdź poprawność dat')


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

    def clean_date_to(self):
        date_to = self.cleaned_data.get('date_to')
        date_from = self.cleaned_data.get('date_from')
        if date_to < date_from:
            raise forms.ValidationError('Sprawdź poprawność dat')


class ContractInsuranceCreateForm(forms.ModelForm):
    class Meta:
        model = ContractInsurance
        fields = "__all__"
        labels = LABELS
        widgets = {'contract': forms.HiddenInput}

    def clean_date_to(self):
        date_to = self.cleaned_data.get('date_to')
        date_from = self.cleaned_data.get('date_from')
        if date_to < date_from:
            raise forms.ValidationError('Sprawdź poprawność dat')


class ContractTicketCreateForm(forms.ModelForm):
    class Meta:
        model = ContractTicket
        fields = "__all__"
        labels = LABELS
        widgets = {
            'contract': forms.HiddenInput,
            'date_departure': DateInput(),
            'date_arrival': DateInput()
        }

    def clean_date_arrival(self):
        date_to = self.cleaned_data.get('date_departure')
        date_from = self.cleaned_data.get('date_arrival')
        if date_to < date_from:
            raise forms.ValidationError('Sprawdź poprawność dat')


class ContractOtherCreateForm(forms.ModelForm):
    class Meta:
        model = ContractOther
        fields = "__all__"
        labels = LABELS
        widgets = {'contract': forms.HiddenInput}

    def clean_date_to(self):
        date_to = self.cleaned_data.get('date_to')
        date_from = self.cleaned_data.get('date_from')
        if date_to < date_from:
            raise forms.ValidationError('Sprawdź poprawność dat')


class VillaCreateForm(forms.ModelForm):
    class Meta:
        model = Villa
        fields = ["region", "name", "size", "rooms_no", "link"]
        labels = LABELS


class UploadForm(forms.ModelForm):
    class Meta:
        model = ContractFile
        fields = ["contract", "pdf"]
        widgets = {
            'contract': forms.HiddenInput,
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        labels = LABELS
        fields = "__all__"
        widgets = {
            'contract': forms.HiddenInput,
            'payment_date': DateInput(),
        }
