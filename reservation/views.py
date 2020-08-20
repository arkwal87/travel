import openpyxl

from datetime import date
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, View, DeleteView, UpdateView
from reservation.models import Client, Hotel, Room, Reservation, RoomReservation, Country, Continent, Region
from reservation.forms import ReservationCreateForm, RoomReservationCreateForm, RoomCreateForm


# ================================== CLIENTS VIEWS =====================================================================

class ClientListView(View):
    def get(self, request):
        columns = ["#", "Imię", "Nazwisko", "Data urodzenia"]
        client_list = Client.objects.all().order_by("pk")
        return render(request, "object_list.html", context={"objects": client_list, "columns": columns})


class ClientCreateView(CreateView):
    model = Client
    fields = "__all__"
    success_url = reverse_lazy("client_list")
    template_name = "create_view.html"


class ClientDetailView(DetailView):
    model = Client
    template_name = "detail_view.html"
    columns = ["#", "Imię", "Nazwisko", "Data urodzenia", "Telefon", "e-mail", "rezerwujący", "uczestnik"]

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Client, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owned_reservations = Reservation.objects.filter(owner=self.kwargs.get("id"))
        context.update({
            "columns": self.columns,
            "owned_reservations": owned_reservations
        })
        return context


class ClientUpdateView(UpdateView):
    model = Client
    fields = "__all__"
    template_name = "update_view.html"
    success_url = reverse_lazy("client_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Client, id=id_)


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "delete_view.html"
    success_url = reverse_lazy("client_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Client, id=id_)


# ==================================== HOTEL VIEWS =====================================================================

class HotelListView(View):
    def get(self, request):
        columns = ["#", "Nazwa", "Kontynent", "Kraj", "Region"]
        hotel_list = Hotel.objects.all().order_by("pk")
        return render(request, "object_list.html", context={"objects": hotel_list, "columns": columns})


class HotelCreateView(CreateView):
    model = Hotel
    fields = "__all__"
    success_url = reverse_lazy("hotel_list")
    template_name = "create_view.html"


class HotelDetailView(DetailView):
    model = Hotel
    template_name = "hotels_view.html"
    columns = ["#", "Nazwa", "Kontynent", "Kraj", "Region", "Link"]
    columns_room = ["#", "Nazwa", "Cena", "Waluta", "Wielkość pokoju", "Wielkość tarasu", "Operacje"]

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Hotel, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"columns": self.columns, "columns_room": self.columns_room})
        return context


class HotelUpdateView(UpdateView):
    model = Hotel
    fields = "__all__"
    template_name = "update_view.html"
    success_url = reverse_lazy("hotel_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Hotel, id=id_)


class HotelDeleteView(DeleteView):
    model = Hotel
    template_name = "delete_view.html"
    success_url = reverse_lazy("hotel_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Hotel, id=id_)


# ==================================== ROOM VIEWS ======================================================================

class RoomListView(View):
    def get(self, request):
        columns = ["#", "Nazwa", "Cena", "Waluta", "Hotel"]
        room_list = Room.objects.all().order_by('pk')
        return render(request, "object_list.html", context={"objects": room_list, "columns": columns})


class RoomCreateView(CreateView):
    model = Room
    fields = "__all__"
    initial = {"name": "Nazwa1"}
    template_name = "create_view.html"
    success_url = reverse_lazy("room_list")


class HotelRoomCreateView(View):
    def get(self, request, pk=None):
        if pk is None:
            form = RoomCreateForm()
        else:
            initial_data = {"hotel": Hotel.objects.get(pk=pk)}
            form = RoomCreateForm(initial=initial_data)
        return render(request, "create_view.html", {"form": form})

    def post(self, request, pk=None):
        if pk is None:
            form = RoomCreateForm(request.POST)
        else:
            initial_data = {"hotel": Hotel.objects.get(pk=pk)}
            form = RoomCreateForm(request.POST, initial=initial_data)
        if form.is_valid:
            form.save()
        return redirect(f"/reservation/hotele/{pk}")


class RoomDetailView(DetailView):
    model = Room
    template_name = "detail_view.html"
    columns = ["#", "Nazwa", "Cena", "Waluta", "Hotel"]

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Room, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"columns": self.columns})
        return context


class RoomUpdateView(UpdateView):
    model = Room
    fields = "__all__"
    template_name = "update_view.html"
    success_url = reverse_lazy("room_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Room, id=id_)


class RoomDeleteView(DeleteView):
    model = Room
    template_name = "delete_view.html"
    success_url = reverse_lazy("room_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Room, id=id_)


# ==================================== RESERVATION VIEWS ===============================================================

class ReservationListView(View):
    def get(self, request):
        columns = ["#", "Zamawiający", "Kierunek", "Data rezerwacji"]
        reservation_list = Reservation.objects.all().order_by('pk')
        return render(request, "object_list.html", context={"objects": reservation_list, "columns": columns})


class ReservationCreateView(CreateView):
    form_class = ReservationCreateForm
    template_name = "create_view.html"
    success_url = reverse_lazy("reservation_list")


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = "reservation_view.html"
    columns = ["#", "Pokoj", "Cena", "Waluta", "Serwis",
               "Data rezerwacji", "Data wyjazdu", "Data powrotu", "Klient"]
    columns2 = ["#", "Pokoj", "Hotel", "Cena", "Waluta", "Data wyjazdu", "Data powrotu"]

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Reservation, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"columns": self.columns, "columns2": self.columns2})
        return context


class ReservationUpdateView(UpdateView):
    model = Reservation
    fields = ("#", "owner", "price_service", "client")
    template_name = "update_view.html"
    success_url = reverse_lazy("reservation_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Reservation, id=id_)


class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = "delete_view.html"
    success_url = reverse_lazy("reservation_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Reservation, id=id_)


# ==================================== ROOM RESERVATION VIEWS ==========================================================

class RoomReservationCreateView(CreateView):
    model = RoomReservation
    fields = "__all__"
    template_name = "create_view.html"
    success_url = reverse_lazy("reservation_list")


class RoomReservationDeleteView(DeleteView):
    model = RoomReservation
    template_name = "delete_view.html"
    success_url = reverse_lazy("reservation_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(RoomReservation, id=id_)


class CreateContractView(View):
    def get(self, request, id):
        my_res = Reservation.objects.get(pk=id)
        row = 46
        my_xl = openpyxl.load_workbook("doc_patterns/instyle.xlsx")
        my_xl["Sheet1"]["P21"].value = my_res.date_of_reservation
        my_xl["Sheet1"]["P26"].value = f"{my_res.get_data[0]} - {my_res.get_data[1]}"
        my_xl["Sheet1"]["B31"].value = f"{my_res.owner.first_name} {my_res.owner.last_name}"
        my_xl["Sheet1"]["P31"].value = my_res.owner.date_of_birth
        my_xl["Sheet1"]["B36"].value = \
            f"{my_res.owner.postcode} {my_res.owner.city}\n{my_res.owner.address}"
        my_xl["Sheet1"]["P36"].value = my_res.owner.phone_number
        for participant in my_res.client.all():
            my_xl["Sheet1"][f"B{row}"] = row - 45
            my_xl["Sheet1"][f"C{row}"] = f"{participant.first_name} {participant.last_name}"
            row += 1
        row = 73
        for room_reservation in RoomReservation.objects.filter(reservation_id=my_res.pk):
            my_xl["Sheet1"][f"B{row}"].value = f'{room_reservation.room.hotel.country.name}, ' \
                                               f'\n{room_reservation.room.hotel.region.name}'
            my_xl["Sheet1"][f"F{row}"].value = f"{room_reservation.date_from} - {room_reservation.date_to}"
            my_xl["Sheet1"][f"J{row}"].value = (room_reservation.date_to - room_reservation.date_from).days
            my_xl["Sheet1"][f"L{row}"].value = room_reservation.room.hotel.name
            my_xl["Sheet1"][f"R{row}"].value = "info o zakwaterowaniu"
            my_xl["Sheet1"][f"W{row}"].value = "info o wyzywieniu"
            row += 4
        total_price = ""
        for name, price in my_res.get_prices.items():
            if total_price != "":
                total_price += " + "
            total_price += f"{price} {name}"
        my_xl["Sheet1"]["J131"].value = total_price
        my_xl.save("doc_patterns/test.xlsx")
        return render(request, "detail_view.html", context={"info": "Utworzono plik z umową!"})


def get_countries_by_continent(request):
    continent_id = request.GET.get('continent_id')
    if continent_id is None:
        countries = Country.objects.all()
    else:
        continent = Continent.objects.get(pk=continent_id)
        countries = Country.objects.filter(continent=continent)
    return render(request, 'rest_list_view.html', {'objects': countries})


def get_regions_by_countries(request):
    country_id = request.GET.get('country_id')
    if country_id is None:
        regions = Region.objects.all()
    else:
        country = Country.objects.get(pk=country_id)
        regions = Region.objects.filter(country=country)
    return render(request, 'rest_list_view.html', {'objects': regions})

# def check_birthday(request):
#     return ""