# -*- coding: utf-8 -*-
import os.path
import os
import openpyxl
import mimetypes

from django.core.management.color import no_style
from django.db import connection

from datetime import date, timedelta

from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, View, DeleteView, UpdateView, TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from reservation.excel_creator import contract_to_excel
from reservation.models import Client, Hotel, Room, Country, Continent, Region, Counterparty, Contract, MealPlan, \
    Reference, Currency, ContractRoom, Villa, ContractVilla, Airline, ContractTrain, Train, ContractInsurance, \
    ContractTicket, ContractOther, ContractFile, Payment
from reservation.forms import RoomCreateForm, HotelCreateForm, ClientCreateForm, CounterpartyCreateForm, \
    VillaCreateForm, \
    ContractRoomCreateForm, ContractVillaCreateForm, ContractTrainCreateForm, ContractInsuranceCreateForm, \
    ContractTicketCreateForm, ContractOtherCreateForm, ContractCreateForm, UploadForm, PaymentForm

from django.core.files.storage import FileSystemStorage


# ================================== CLIENTS VIEWS =====================================================================

class MyTemplateView(TemplateView):
    template_name = "home.html"

    def get_birthday_3(self):
        check_date = date.today()
        birthday_list = [[], [], []]
        for client in Client.objects.all():
            if client.date_of_birth is not None:
                birthday_date = client.date_of_birth.replace(year=check_date.year)
            if birthday_date == check_date:
                birthday_list[0].append(client)
            elif check_date < birthday_date < (check_date + timedelta(days=8)):
                birthday_list[1].append(client)
            elif (check_date + timedelta(days=7)) < birthday_date < (check_date + timedelta(days=22)):
                birthday_list[2].append(client)
        return birthday_list

    def get_unpaid_contracts(self):
        today = date.today()
        contract_list = Contract.objects.filter(payment_deadline__gt=today-timedelta(days=14))
        return contract_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "birthday_list": self.get_birthday_3(),
            "contract_list": self.get_unpaid_contracts()
        })
        return context


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client/client_list_view.html"
    ordering = ['last_name']
    columns = ["Nazwisko", "Imię", "Data urodzenia", "Telefon", "e-mail", "Źródło", "Lider"]

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        context['columns'] = self.columns
        return context


class ClientCreateView(CreateView):
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
    columns = ["Nazwa", "Kategoria", "Kontynent", "Kraj", "Region"]
    ordering = ["name"]
    template_name = "hotel/hotel_list_view.html"

    def get_context_data(self, **kwargs):
        context = super(HotelListView, self).get_context_data(**kwargs)
        context['columns'] = self.columns
        return context


class HotelCreateView(LoginRequiredMixin, CreateView):
    form_class = HotelCreateForm
    success_url = reverse_lazy("hotel_list")
    template_name = "hotel\hotel_create_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"continents": Continent.objects.all(), "countries": Country.objects.all()})
        return context


class HotelDetailView(LoginRequiredMixin, DetailView):
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


class HotelUpdateView(LoginRequiredMixin, UpdateView):
    form_class = HotelCreateForm
    success_url = reverse_lazy("hotel_list")
    template_name = "update_view.html"

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Hotel, id=id_)


class HotelDeleteView(LoginRequiredMixin, DeleteView):
    model = Hotel
    template_name = "delete_view.html"
    success_url = reverse_lazy("hotel_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Hotel, id=id_)


# ==================================== ROOM VIEWS ======================================================================


class HotelRoomCreateView(LoginRequiredMixin, View):
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


class RoomDetailView(LoginRequiredMixin, DetailView):
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


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    # model = Room
    form_class = RoomCreateForm
    # fields = "__all__"
    template_name = "update_view.html"
    success_url = reverse_lazy("room_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Room, id=id_)


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = "delete_view.html"
    success_url = reverse_lazy("room_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Room, id=id_)


# ==================================== COUNTERPARTY VIEWS ==============================================================

class CounterpartyListView(LoginRequiredMixin, ListView):
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


class CounterpartyCreateView(LoginRequiredMixin, CreateView):
    form_class = CounterpartyCreateForm
    success_url = reverse_lazy("counterparty_list")
    template_name = "standard_create_view.html"


class CounterpartyDetailView(LoginRequiredMixin, DetailView):
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


class CounterpartyUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CounterpartyCreateForm
    success_url = reverse_lazy("counterparty_list")
    template_name = "update_view.html"

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Counterparty, id=id_)


class CounterpartyDeleteView(LoginRequiredMixin, DeleteView):
    model = Counterparty
    template_name = "delete_view.html"
    success_url = reverse_lazy("counterparty_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Counterparty, id=id_)


# ==================================== CONTRACT VIEWS ==========================================================

class ContractListView(LoginRequiredMixin, ListView):
    model = Contract
    columns = ["#", "Data rezerwacji", "Data od", "Data do", "Właściciel"]
    template_name = "contract/contract_list_view.html"

    def get_context_data(self, **kwargs):
        context = super(ContractListView, self).get_context_data(**kwargs)
        context["columns"] = self.columns
        return context


class ContractCreateView(LoginRequiredMixin, CreateView):
    form_class = ContractCreateForm
    template_name = "standard_create_view.html"
    success_url = reverse_lazy("contract_list")

    def form_valid(self, form):
        self.object = form.save()
        contract_daily_id = len(Contract.objects.filter(date_of_contract=self.object.date_of_contract))
        self.object.name = f'IST/{self.object.date_of_contract.strftime("%y%m%d")}/{contract_daily_id:02d}'
        form.save()
        return super().form_valid(form)


class ContractDetailView(LoginRequiredMixin, DetailView):
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
        context.update({
            "columns": self.columnsRoom,
            "payments": Payment.objects.filter(contract=get_object_or_404(Contract, id=self.kwargs.get("id"))),
            "files": ContractFile.objects.filter(contract=self.object)
        })
        return context


class ContractUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ContractCreateForm
    template_name = "update_view.html"
    success_url = reverse_lazy("contract_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Contract, id=id_)

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.pk})


class ContractDeleteView(LoginRequiredMixin, DeleteView):
    model = Contract
    template_name = "delete_view.html"
    success_url = reverse_lazy("contract_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Contract, id=id_)


class UploadView(CreateView):
    model = ContractFile
    form_class = UploadForm
    template_name = "upload_file.html"

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract.id})

    def get_initial(self):
        return {'contract': get_object_or_404(Contract, id=self.kwargs.get("id"))}

    def form_valid(self, form):
        self.object = form.save()
        self.object.file_name = f'{str(self.object.pdf).replace("pdfs/", "")}'
        form.save()
        return super().form_valid(form)


#
# def uploadFile(request, id):
#     if request.method == "POST":
#         form = UploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("contract_list")
#             # return reverse_lazy("contract_detail_view", kwargs={'id': id})
#     else:
#         form = UploadForm()
#     return render(request, "upload_file.html", {'form': form})


# ==================================================== VILLA VIEWS =====================================================


class VillaListView(LoginRequiredMixin, ListView):
    model = Villa
    columns = ["Nazwa", "Powierzchnia", "Liczba pokoi", "Kontynent", "Kraj", "Region"]
    template_name = "villa/villa_list_view.html"

    def get_context_data(self, **kwargs):
        context = super(VillaListView, self).get_context_data(**kwargs)
        context['columns'] = self.columns
        return context


class VillaCreateView(LoginRequiredMixin, CreateView):
    form_class = VillaCreateForm
    success_url = reverse_lazy("villa_list")
    template_name = "villa/villa_create_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"continents": Continent.objects.all(), "countries": Country.objects.all()})
        return context


class VillaDetailView(LoginRequiredMixin, DetailView):
    model = Villa
    template_name = "villa/villa_detail_view.html"
    columns = ["Nazwa", "Powierzchnia", "Liczba pokoi", "Kontynent", "Kraj", "Region", "Link"]

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Villa, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contract_list = ContractVilla.objects.filter(villa=get_object_or_404(Villa, id=self.kwargs.get("id"))).distinct(
            "contract_id")
        context.update({"columns": self.columns, "contract_list": contract_list})
        context.update({"columns": self.columns})
        return context


class VillaUpdateView(LoginRequiredMixin, UpdateView):
    # model = Villa
    # fields = "__all__"
    # template_name = "update_view.html"
    # success_url = reverse_lazy("villa_list")

    form_class = VillaCreateForm
    success_url = reverse_lazy("villa_list")
    template_name = "update_view.html"

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Villa, id=id_)


class VillaDeleteView(LoginRequiredMixin, DeleteView):
    model = Villa
    template_name = "delete_view.html"
    success_url = reverse_lazy("villa_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Villa, id=id_)


# ==================================================== TRAIN VIEWS =====================================================


class TrainListView(LoginRequiredMixin, ListView):
    model = Train
    columns = ["Nazwa", "Miasto początkowe", "Miasto docelowe"]
    template_name = "train/train_list_view.html"

    def get_context_data(self, **kwargs):
        context = super(TrainListView, self).get_context_data(**kwargs)
        context['columns'] = self.columns
        return context


class TrainDetailView(LoginRequiredMixin, DetailView):
    model = Train
    template_name = "train/train_detail_view.html"

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Train, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contract_list = ContractTrain.objects.filter(train=get_object_or_404(Train, id=self.kwargs.get("id"))).distinct(
            "contract_id")
        context.update({"contract_list": contract_list})
        return context


class TrainCreateView(LoginRequiredMixin, CreateView):
    model = Train
    fields = '__all__'
    success_url = reverse_lazy("train_list")
    template_name = "train/train_create_view.html"


class TrainUpdateView(LoginRequiredMixin, UpdateView):
    model = Train
    fields = '__all__'
    success_url = reverse_lazy("train_list")
    template_name = "update_view.html"

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Train, pk=id_)


class TrainDeleteView(LoginRequiredMixin, DeleteView):
    model = Train
    template_name = "delete_view.html"
    success_url = reverse_lazy("train_list")

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Train, id=id_)


# ========================================= CONTRACTS DETAIL VIEWS =====================================================

class ContractRoomCreateView(LoginRequiredMixin, CreateView):
    form_class = ContractRoomCreateForm
    template_name = "contract/contract_prod_create_view.html"
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


class ContractRoomUpdateView(LoginRequiredMixin, UpdateView):
    model = ContractRoom
    fields = "__all__"
    template_name = "update_view.html"

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(ContractRoom, pk=id_)


class ContractRoomDeleteView(LoginRequiredMixin, DeleteView):
    model = ContractRoom
    template_name = "delete_view.html"

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(ContractRoom, pk=id_)


class ContractVillaCreateView(LoginRequiredMixin, CreateView):
    form_class = ContractVillaCreateForm
    template_name = "contract/contract_prod_create_view.html"
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


class ContractVillaUpdateView(LoginRequiredMixin, UpdateView):
    model = ContractVilla
    fields = "__all__"
    template_name = "update_view.html"

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(ContractVilla, pk=id_)


class ContractVillaDeleteView(LoginRequiredMixin, DeleteView):
    model = ContractVilla
    template_name = "delete_view.html"

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(ContractVilla, pk=id_)


class ContractTrainCreateView(LoginRequiredMixin, CreateView):
    form_class = ContractTrainCreateForm
    template_name = "contract/contract_prod_create_view.html"
    success_url = reverse_lazy("contract_train_create")

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_initial(self):
        return {'contract': get_object_or_404(Contract, id=self.kwargs.get("id"))}


class ContractTrainUpdateView(LoginRequiredMixin, UpdateView):
    model = ContractTrain
    fields = "__all__"
    template_name = "update_view.html"

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(ContractTrain, pk=id_)


class ContractTrainDeleteView(LoginRequiredMixin, DeleteView):
    model = ContractTrain
    template_name = "delete_view.html"

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(ContractTrain, pk=id_)


class ContractInsuranceCreateView(LoginRequiredMixin, CreateView):
    form_class = ContractInsuranceCreateForm
    template_name = "contract/contract_prod_create_view.html"
    success_url = reverse_lazy("contract_insurance_create")

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_initial(self):
        return {'contract': get_object_or_404(Contract, id=self.kwargs.get("id"))}


class ContractInsuranceUpdateView(LoginRequiredMixin, UpdateView):
    model = ContractInsurance
    fields = "__all__"
    template_name = "update_view.html"

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(ContractInsurance, pk=id_)


class ContractInsuranceDeleteView(LoginRequiredMixin, DeleteView):
    model = ContractInsurance
    template_name = "delete_view.html"

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(ContractInsurance, pk=id_)


class ContractTicketCreateView(LoginRequiredMixin, CreateView):
    form_class = ContractTicketCreateForm
    template_name = "contract/contract_prod_create_view.html"
    success_url = reverse_lazy("contract_ticket_create")

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_initial(self):
        return {'contract': get_object_or_404(Contract, id=self.kwargs.get("id"))}


class ContractTicketUpdateView(LoginRequiredMixin, UpdateView):
    model = ContractTicket
    fields = "__all__"
    template_name = "update_view.html"

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(ContractTicket, pk=id_)


class ContractTicketDeleteView(LoginRequiredMixin, DeleteView):
    model = ContractTicket
    template_name = "delete_view.html"

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(ContractTicket, pk=id_)


class ContractTicketDetailView(LoginRequiredMixin, DetailView):
    model = ContractTicket
    template_name = "ticket/ticket_detail_view.html"

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(ContractTicket, id=id_)


class ContractOtherCreateView(LoginRequiredMixin, CreateView):
    form_class = ContractOtherCreateForm
    template_name = "contract/contract_prod_create_view.html"
    success_url = reverse_lazy("contract_other_create")

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_initial(self):
        return {'contract': get_object_or_404(Contract, id=self.kwargs.get("id"))}


class ContractOtherUpdateView(LoginRequiredMixin, UpdateView):
    model = ContractOther
    fields = "__all__"
    template_name = "update_view.html"

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(ContractOther, pk=id_)


class ContractOtherDeleteView(LoginRequiredMixin, DeleteView):
    model = ContractOther
    template_name = "delete_view.html"

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(ContractOther, pk=id_)


class ContractOtherDetailView(LoginRequiredMixin, DetailView):
    model = ContractOther
    template_name = "other/other_detail_view.html"

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("id")
        return get_object_or_404(ContractOther, id=id_)


# ==================================== PAYMENT VIEWS  ==================================================================

class PaymentCreateView(LoginRequiredMixin, CreateView):
    form_class = PaymentForm
    template_name = "contract/contract_prod_create_view.html"

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})

    def get_initial(self):
        return {'contract': get_object_or_404(Contract, id=self.kwargs.get("id"))}


class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PaymentForm
    template_name = "update_view.html"

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Payment, pk=id_)

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})


class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = "delete_view.html"

    def get_object(self, **kwargs):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Payment, pk=id_)

    def get_success_url(self):
        return reverse_lazy("contract_detail_view", kwargs={'id': self.object.contract})


class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    columns = ["Kontrakt", "Data wpłaty", "Wartość", "Waluta"]
    template_name = "payment/payment_list_view.html"

    def get_context_data(self, **kwargs):
        context = super(PaymentListView, self).get_context_data(**kwargs)
        context['columns'] = self.columns
        return context


# ==================================== CREATE DOCUMENT =================================================================

class CreateContractView(LoginRequiredMixin, View):
    def get(self, request, id):
        contract_to_excel(id)
        return render(request, "detail_view_xls.html", context={"info": "Utworzono plik z umową!"})


def upload(request):
    # print(MEDIA_ROOT)
    if request.method == "POST":
        uploading_file = request.FILES["document"]
        fs = FileSystemStorage()
        fs.save(uploading_file.name, uploading_file)
    return render(request, 'upload.html')


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


def get_villas_by_regions(request):
    region_id = request.GET.get("region_id")
    if region_id == "" or region_id is None:
        villas = Villa.objects.all()
    else:
        region = Region.objects.get(pk=region_id)
        villas = Villa.objects.filter(region=region)
    return render(request, "rest_list_view.html", {"objects": villas})


def get_rooms_by_hotels(request):
    hotel_id = request.GET.get("hotel_id")
    if hotel_id is None or hotel_id == "":
        rooms = Room.objects.all()
    else:
        hotel = Hotel.objects.get(pk=hotel_id)
        rooms = Room.objects.filter(hotel=hotel)
    return render(request, "rest_list_view.html", {"objects": rooms})


# class DownloadView(LoginRequiredMixin, View):
#     def get(self, request):
#         base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         filename = "test.xlsx"
#         filepath = base_dir + "/docs/" + filename
#         thefile = filepath
#         filename = os.path.basename(thefile)
#         chunk_size = 8192
#         response = StreamingHttpResponse(FileWrapper(open(thefile, 'rb'), chunk_size),
#                                          content_type=mimetypes.guess_type(thefile)[0])
#         response['Content-Length'] = os.path.getsize(thefile)
#         response['Content-Disposition'] = "Attachment;filename=%s" % filename
#         return render(request)
#
#     def post(self, request, pk=None):
#         # if pk is None:`
#         #     form = RoomCreateForm(request.POST)
#         # else:
#         #     initial_data = {"hotel": Hotel.objects.get(pk=pk)}
#         #     form = RoomCreateForm(request.POST, initial=initial_data)
#         # if form.is_valid:
#         #     form.save()
#         # return redirect(f"/reservation/hotele/{pk}")
#         return None


@login_required
def downloadFile(request, id):
    contract_to_excel(id)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = Contract.objects.get(id=id).name.replace("/", "_")
    filepath = base_dir + "/media/" + filename + ".xlsx"
    thefile = filepath
    filename = os.path.basename(filepath)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(thefile, 'rb'), chunk_size),
                                     content_type=mimetypes.guess_type(thefile)[0])
    response['Content-Length'] = os.path.getsize(thefile)
    response['Content-Disposition'] = "Attachment;filename=%s" % filename
    return response


@login_required
def downloadPdf(request, id):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = ContractFile.objects.get(id=id).pdf
    # print(filename)
    filepath = base_dir + "/media/" + str(filename)
    thefile = filepath
    filename = os.path.basename(filepath)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(thefile, 'rb'), chunk_size),
                                     content_type=mimetypes.guess_type(thefile)[0])
    response['Content-Length'] = os.path.getsize(thefile)
    response['Content-Disposition'] = "Attachment;filename=%s" % filename
    return response


@login_required
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
        'Villa': Villa,
        'Airline': Airline
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
                elif modelName == "Villa":
                    if field.name == "region":
                        to_insert[field.name] = Region.objects.get(name=row[j].value)
                    else:
                        to_insert[field.name] = row[j].value
                else:
                    to_insert[field.name] = row[j].value
            m = modelObj(**to_insert)
            m.save()

            sequence_sql = connection.ops.sequence_reset_sql(no_style(), list(modelsDict.values()))
            with connection.cursor() as cursor:
                for sql in sequence_sql:
                    cursor.execute(sql)

    return render(request, "test_view.html", {'tab_names': tab_names})
