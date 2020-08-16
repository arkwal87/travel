from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, View, DeleteView, UpdateView
from reservation.models import Client, Hotel, Room, Reservation, RoomReservation
from reservation.forms import ReservationCreateForm


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
                   "Data rezerwacji"]  # , "Data wylotu", "Data powrotu", "Klient"]
        reservation_list = Reservation.objects.all().order_by('pk')
        return render(request, "object_list.html", context={"objects": reservation_list, "columns": columns})


class ReservationCreateView(CreateView):
    model = Reservation
    fields = ("price_service", "client")
    template_name = "create_view.html"
    success_url = reverse_lazy("reservation_list")


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = "reservation_view.html"
    columns = ["#", "Pokoj", "Cena", "Waluta", "Serwis",
               "Data rezerwacji", "Data wylotu", "Data powrotu", "Klient"]
    columns2 = ["#", "Pokoj", "Hotel", "Cena", "Waluta", "Data wylotu", "Data powrotu"]

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Reservation, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"columns": self.columns, "columns2": self.columns2})
        return context


class ReservationUpdateView(UpdateView):
    model = Reservation
    fields = "__all__"
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


#
# class NewReservation(View):
#     def get(self, request):
#         return render(request, "new_reservation_view.html", {"hotels_list": Hotel.objects.all()})
#
#
#     def post(self, request):
#         print(Room.objects.filter(hotel=Hotel.objects.get(name=request.POST["hotels"])))
#         form = ReservationCreateForm
#         return render(request, f"new_create.html", {"form":form})

# ==================================== ROOM RESERVATION VIEWS ==========================================================

class RoomReservationCreateView(CreateView):

    model = RoomReservation
    fields = "__all__"
    template_name = "create_view.html"
    success_url = reverse_lazy("reservation_list")

