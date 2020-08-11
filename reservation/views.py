from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, View, DeleteView, UpdateView
from reservation.models import Client, Hotel


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"info": "This is view for creating a new client"})
        return context


class ClientDetailView(DetailView):
    model = Client
    template_name = "detail_view.html"
    columns = ["#", "Imię", "Nazwisko", "Data urodzenia", "Telefon", "e-mail"]

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Client, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"columns": self.columns})
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"info": "This is view for creating a new hotel"})
        return context


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