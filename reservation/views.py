# -*- coding: utf-8 -*-

import openpyxl

from datetime import date, datetime, timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, View, DeleteView, UpdateView, TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from reservation.models import Client, Hotel, Room, Country, Continent, Region, Counterparty, Contract, MealPlan, \
    Reference, Currency, ContractRoom, Villa
from reservation.forms import RoomCreateForm, HotelCreateForm, ClientCreateForm, CounterpartyCreateForm, \
    VillaCreateForm, \
    ContractRoomCreateForm, ContractVillaCreateForm


# ================================== CLIENTS VIEWS =====================================================================

class MyTemplateView(TemplateView):
    template_name = "index.html"

    def get_birthday_3(self):
        check_date = date.today()
        birthday_list = [[], [], []]
        for client in Client.objects.all():
            if check_date.month == client.date_of_birth.month and check_date.day == client.date_of_birth.day:
                birthday_list[0].append(client)
            elif (check_date + timedelta(days=7)).month == client.date_of_birth.month and \
                    (check_date + timedelta(days=7)).day == client.date_of_birth.day:
                birthday_list[1].append(client)
            elif (check_date + timedelta(days=21)).month == client.date_of_birth.month and \
                    (check_date + timedelta(days=21)).day == client.date_of_birth.day:
                birthday_list[2].append(client)
        return birthday_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        birthday_list = self.get_birthday_3()
        context.update({"birthday_list": birthday_list})
        return context


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client/client_list_view.html"
    ordering = ['last_name']
    # paginate_by = 5
    columns = ["Nazwisko", "Imię", "Data urodzenia", "Telefon", "e-mail", "Źródło", "Lider"]

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        context['columns'] = self.columns
        return context


class ClientCreateView(CreateView):
    # model = Client
    # fields = "__all__"
    form_class = ClientCreateForm
    success_url = reverse_lazy("client_list")
    template_name = "standard_create_view.html"


class ClientDetailView(DetailView):
    model = Client
    template_name = "client/client_detail_view.html"

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Client, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owned_contracts = Contract.objects.filter(owner=self.kwargs.get("id"))
        context.update({"owned_contracts": owned_contracts})
        return context


class ClientUpdateView(UpdateView):
    form_class = ClientCreateForm
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

class HotelListView(LoginRequiredMixin, ListView):
    model = Hotel
    columns = ["Nazwa", "Kontynent", "Kraj", "Region"]
    ordering = ["name"]
    template_name = "hotel/hotel_list_view.html"

    def get_context_data(self, **kwargs):
        context = super(HotelListView, self).get_context_data(**kwargs)
        context['columns'] = self.columns
        return context


class HotelCreateView(CreateView):
    # model = Hotel
    form_class = HotelCreateForm
    # fields = "__all__"
    success_url = reverse_lazy("hotel_list")
    template_name = "hotel\hotel_create_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"continents": Continent.objects.all(), "countries": Country.objects.all()})
        return context


class HotelDetailView(DetailView):
    model = Hotel
    template_name = "hotel/hotel_detail_view.html"
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


class HotelRoomCreateView(View):
    def get(self, request, pk=None):
        if pk is None:
            form = RoomCreateForm()
        else:
            initial_data = {"hotel": Hotel.objects.get(pk=pk)}
            form = RoomCreateForm(initial=initial_data)
        return render(request, "standard_create_view.html", {"form": form})

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
    template_name = "hotel/room_detail_view.html"
    columns = ["#", "Nazwa", "Cena", "Waluta", "Hotel"]

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Room, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contract_list = ContractRoom.objects.filter(room=get_object_or_404(Room, id=self.kwargs.get("id"))).distinct(
            "contract_id")
        context.update({"columns": self.columns, "contract_list": contract_list})
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


# ==================================== COUNTERPARTY VIEWS ==============================================================

class CounterpartyListView(ListView):
    model = Counterparty
    columns = ["Nazwa", "Pełna nazwa", "nr VAT", "Kraj", "Kod pocztowy", "Miasto", "Adres"]
    ordering = ["short_name"]
    template_name = "counterparty/counterparty_list_view.html"

    def get_context_data(self, **kwargs):
        # context = super(CounterpartyListView, self).get_context_data(**kwargs)
        context = super().get_context_data()
        context.update({"columns": self.columns})
        # context['columns'] = self.columns
        return context


class CounterpartyCreateView(CreateView):
    form_class = CounterpartyCreateForm
    success_url = reverse_lazy("counterparty_list")
    template_name = "standard_create_view.html"


class CounterpartyDetailView(DetailView):
    model = Counterparty
    columns = ["Nazwa", "Pełna nazwa", "nr VAT", "Kraj", "Kod pocztowy", "Miasto", "Adres"]
    template_name = "counterparty/counterparty_detail_view.html"

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Counterparty, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_contracts = ContractRoom.objects.filter(
            counterparty=get_object_or_404(Counterparty, id=self.kwargs.get("id")))
        context.update(
            {
                "unique_contracts": unique_contracts.distinct("contract_id"),
                "columns": self.columns
            }
        )
        return context

    @property
    def get_products_number(self, **kwargs):
        my_id = self.object.pk
        my_list = ContractRoom.objects.filter()
        return


class CounterpartyUpdateView(UpdateView):
    model = Counterparty
    fields = "__all__"
    template_name = "update_view.html"
    success_url = reverse_lazy("counterparty_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Counterparty, id=id_)


class CounterpartyDeleteView(DeleteView):
    model = Room
    template_name = "delete_view.html"
    success_url = reverse_lazy("counterparty_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Counterparty, id=id_)


# ==================================== CONTRACT VIEWS ==========================================================

class ContractListView(ListView):
    model = Contract
    columns = ["#", "Data rezerwacji", "Data od", "Data do", "Właściciel"]
    template_name = "contract/contract_list_view.html"

    def get_context_data(self, **kwargs):
        context = super(ContractListView, self).get_context_data(**kwargs)
        context["columns"] = self.columns
        return context


class ContractCreateView(CreateView):
    model = Contract
    fields = "__all__"
    template_name = "standard_create_view.html"
    success_url = reverse_lazy("contract_list")


class ContractDetailView(DetailView):
    model = Contract
    template_name = "contract/contract_detail_view.html"
    columnsRoom = ["Nazwa", "Data od", "Data do", "Kategoria", "Liczba pokoi", "Cena oferty", "Waluta", "Cena net",
                   "Waluta",
                   "Kontrahent", "Meal Plan"]

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Contract, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"columns": self.columnsRoom})
        return context


class ContractUpdateView(UpdateView):
    model = Contract
    fields = "__all__"
    template_name = "update_view.html"

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Contract, id=id_)

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.pk})


# ==================================================== VILLA VIEWS =====================================================


class VillaListView(LoginRequiredMixin, ListView):
    model = Villa
    columns = ["Nazwa", "Powierzchnia", "Liczba pokoi", "Basen", "Kontynent", "Kraj", "Region"]
    # ordering = ["id"]
    template_name = "villa/villa_list_view.html"

    def get_context_data(self, **kwargs):
        context = super(VillaListView, self).get_context_data(**kwargs)
        context['columns'] = self.columns
        return context


class VillaCreateView(LoginRequiredMixin, CreateView):
    # model = Hotel
    form_class = VillaCreateForm
    # fields = "__all__"
    success_url = reverse_lazy("villa_list")
    template_name = "villa/villa_create_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"continents": Continent.objects.all(), "countries": Country.objects.all()})
        return context


class VillaDetailView(DetailView):
    model = Villa
    template_name = "villa/villa_detail_view.html"
    columns = ["Nazwa", "Powierzchnia", "Liczba pokoi", "Basen", "Kontynent", "Kraj", "Region", "Link"]

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Villa, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"columns": self.columns})
        return context


class VillaUpdateView(UpdateView):
    model = Villa
    fields = "__all__"
    template_name = "update_view.html"
    success_url = reverse_lazy("villa_list")


#
#     def get_object(self, **kwargs):
#         id_ = self.kwargs.get("id")
#         return get_object_or_404(Hotel, id=id_)
#
#
# class VillaDeleteView(DeleteView):
#     model = Hotel
#     template_name = "delete_view.html"
#     success_url = reverse_lazy("hotel_list")
#
#     def get_object(self, **kwargs):
#         id_ = self.kwargs.get("id")
#         return get_object_or_404(Hotel, id=id_)


# ========================================= CONTRACTS DETAIL VIEWS =====================================================

class ContractRoomCreateView(CreateView):
    form_class = ContractRoomCreateForm
    template_name = "contract/contract_room_create_view.html"
    success_url = reverse_lazy("contract_room_create")
    context_upd = {
        "continents": Continent.objects.all(),
        "countries": Country.objects.all(),
        "regions": Region.objects.all(),
        "hotels": Hotel.objects.all()
    }

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.context_upd)
        return context

    def get_initial(self):
        return {'contract': get_object_or_404(Contract, id=self.kwargs.get("id"))}


class ContractVilaCreateView(CreateView):
    form_class = ContractVillaCreateForm
    template_name = "contract/contract_room_create_view.html"
    success_url = reverse_lazy("contract_room_create")
    context_upd = {
        "continents": Continent.objects.all(),
        "countries": Country.objects.all(),
        "regions": Region.objects.all()
    }

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.context_upd)
        return context

    def get_initial(self):
        return {'contract': get_object_or_404(Contract, id=self.kwargs.get("id"))}


# ==================================== EXTRA FUNCTIONS =================================================================


def datatables_lang(request):
    return render(request, 'datatables_language.json')


def get_countries_by_continent(request):
    continent_id = request.GET.get('continent_id')
    if continent_id == "" or continent_id is None:
        countries = Country.objects.all()
    else:
        continent = Continent.objects.get(pk=continent_id)
        countries = Country.objects.filter(continent=continent)
    return render(request, 'rest_list_view.html', {'objects': countries})


def get_regions_by_countries(request):
    country_id = request.GET.get('country_id')
    print(country_id)
    if country_id == "" or country_id is None:
        regions = Region.objects.all()
    else:
        country = Country.objects.get(pk=country_id)
        regions = Region.objects.filter(country=country)
    return render(request, 'rest_list_view.html', {'objects': regions})


def get_hotels_by_regions(request):
    region_id = request.GET.get("region_id")
    if region_id == "" or region_id is None:
        hotels = Hotel.objects.all()
    else:
        region = Region.objects.get(pk=region_id)
        hotels = Hotel.objects.filter(region=region)
    return render(request, "rest_list_view.html", {"objects": hotels})


def get_rooms_by_hotels(request):
    hotel_id = request.GET.get("hotel_id")
    if hotel_id is None or hotel_id == "":
        rooms = Room.objects.all()
    else:
        hotel = Hotel.objects.get(pk=hotel_id)
        rooms = Room.objects.filter(hotel=hotel)
    return render(request, "rest_list_view.html", {"objects": rooms})


def populate_db(request):
    modelsDict = {
        'MealPlan': MealPlan,
        'Reference': Reference,
        'Client': Client,
        'Currency': Currency,
        'Continent': Continent,
        'Country': Country,
        'Region': Region,
        'Counterparty': Counterparty,
        'Hotel': Hotel,
        'Room': Room,
    }

    wb = openpyxl.load_workbook("data_db.xlsx")
    tab_names = wb.sheetnames

    for modelName, modelObj in modelsDict.items():
        ws = wb[modelName]
        to_insert = {}
        iterRows = iter(ws.rows)
        next(iterRows)
        for i, row in enumerate(iterRows):
            for j, field in enumerate(modelsDict[modelName]._meta.fields):
                if modelName == "Client":
                    if field.name == "date_of_birth":
                        to_insert[field.name] = row[j].value.date()
                    elif field.name == "reference":
                        to_insert[field.name] = Reference.objects.get(name=row[j].value)
                    else:
                        to_insert[field.name] = row[j].value
                elif modelName == "Country":
                    if field.name == "continent":
                        to_insert[field.name] = Continent.objects.get(name=row[j].value)
                    else:
                        to_insert[field.name] = row[j].value
                elif modelName == "Region":
                    if field.name == "country":
                        to_insert[field.name] = Country.objects.get(name=row[j].value)
                    else:
                        to_insert[field.name] = row[j].value
                elif modelName == "Hotel":
                    if field.name == "region":
                        to_insert[field.name] = Region.objects.get(name=row[j].value)
                    else:
                        to_insert[field.name] = row[j].value
                elif modelName == "Room":
                    if field.name == "hotel":
                        to_insert[field.name] = Hotel.objects.get(name=row[j].value)
                    else:
                        to_insert[field.name] = row[j].value
                else:
                    to_insert[field.name] = row[j].value
            m = modelObj(**to_insert)
            # if modelName == "Client":
            #     print(m.date_of_birth)
            m.save()

    return render(request, "test_view.html", {'tab_names': tab_names})
