import openpyxl
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, View, DeleteView, UpdateView
from reservation.models import Client, Hotel, Room, Reservation, RoomReservation
from reservation.forms import ReservationCreateForm, RoomReservationCreateForm


# ================================== CLIENTS VIEWS =====================================================================

class ClientListView(View):
    def get(self, request):
        columns = ["#", "Imię", "Nazwisko", "Data urodzenia", "Telefon", "e-mail", "Operacje"]
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
    columns = ["#", "Imię", "Nazwisko", "Data urodzenia", "Telefon", "e-mail", "rezerwacje"]

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Client, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_reservations = Client.objects.get(id=self.kwargs.get("id")).reservation_set.all()
        context.update({"columns": self.columns, "my_reservations": my_reservations})
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
    template_name = "detail_view.html"
    columns = ["#", "Nazwa", "Kontynent", "Kraj", "Region", "Link"]

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Hotel, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"columns": self.columns})
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
    template_name = "create_view.html"
    success_url = reverse_lazy("room_list")


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
        columns = ["#", "Pokoj", "Cena", "Waluta", "Serwis",
                   "Data rezerwacji"]
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
    fields = ("owner", "price_service", "client")
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
    # fields = ["room", "date_from", "date_to", "price", "currency"]
    fields = "__all__"
    # form_class = RoomReservationCreateForm(instance=)
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
        my_client = my_res.owner
        row = 46
        my_xl = openpyxl.load_workbook("doc_patterns/instyle.xlsx")
        my_xl["Sheet1"]["P21"].value = my_res.date_of_reservation
        my_xl["Sheet1"]["P26"].value = f"{my_res.get_data[0]} - {my_res.get_data[1]}"
        my_xl["Sheet1"]["B31"].value = f"{my_client.first_name} {my_client.last_name}"
        my_xl["Sheet1"]["P31"].value = my_client.date_of_birth
        my_xl["Sheet1"]["B36"].value = \
            f"{my_client.postcode} {my_client.city}\n{my_client.address}"
        my_xl["Sheet1"]["P36"].value = my_client.phone_number
        for participant in my_res.client.all():
            my_xl["Sheet1"][f"B{row}"]= row-45
            my_xl["Sheet1"][f"C{row}"] = f"{participant.first_name} {participant.last_name}"
            row += 1
        my_xl.save("doc_patterns/test.xlsx")
        return render(request, "object_list.html")
