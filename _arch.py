# ====================== MODELS ========================================================================================


# class Reservation2(models.Model):
#     date_of_reservation = models.DateField()
#     date_from = models.DateField()
#     date_to = models.DateField()
#     hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
#     room_category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
#     room_number = models.PositiveIntegerField(default=1, validators=[MinValueValidator(2)])
#     price_offer = models.DecimalField(max_digits=10, decimal_places=2)
#     price_net = models.DecimalField(max_digits=10, decimal_places=2)
#     offer_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="offer_currency2")
#     net_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="net_currency2")
#     counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE)
#     meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
#
#     def get_nights_number(self):
#         myNo = abs((self.date_to - self.date_from).days)
#         return myNo


# class RoomReservation(models.Model):
#     room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
#     date_from = models.DateField()
#     date_to = models.DateField()
#     price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
#     reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)
#
#     def get_delete_url(self):
#         return f"/reservation/usun_rez_pokoju/{self.pk}/"


# class Reservation(models.Model):
#     price_service = models.DecimalField(decimal_places=2, max_digits=10, null=True)
#     date_of_reservation = models.DateField(auto_now_add=True, blank=True)
#     client = models.ManyToManyField(Client, related_name="reservation_set")
#     owner = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="reservation_owner", null=True)
#
#     def __str__(self):
#         return f"Numer {self.pk}"
#
#     @property
#     def get_dates(self):
#         if RoomReservation.objects.filter(reservation=self).exists():
#             date_from = RoomReservation.objects.filter(reservation=self).order_by("date_from").first().date_from
#             date_to = RoomReservation.objects.filter(reservation=self).order_by("date_to").last().date_to
#             return [date_from, date_to]
#
#     @property
#     def get_prices(self):
#         all_prices = {}
#         # for room_res in RoomReservation.objects.filter(reservation=self):
#         #     if room_res.room.currency.hash in all_prices:
#         #         all_prices[room_res.room.currency.hash] += room_res.room.price
#         #     else:
#         #         all_prices[room_res.room.currency.hash] = room_res.room.price
#         return all_prices
#
#     def get_detail_url(self):
#         return f"/reservation/{self.pk}"
#
#     def get_update_url(self):
#         return f"/reservation/{self.pk}/edytuj"
#
#     def get_delete_url(self):
#         return f"/reservation/{self.pk}/usun"
#
#     def get_unique_regions(self):
#         regions = []
#         for i in RoomReservation.objects.filter(reservation=self).distinct("room"):
#             if i.room.hotel.region not in regions:
#                 regions.append(i.room.hotel.region)
#         return regions
# class Payment(models.Model):
#     reservation_no = models.ForeignKey("Reservation", on_delete=models.SET_NULL, null=True)
#     paid = models.BooleanField(default=False)


# ====================== VIEWS =========================================================================================

# class RoomListView(View):
#     def get(self, request):
#         columns = ["#", "Nazwa", "Cena", "Waluta", "Hotel"]
#         room_list = Room.objects.all().order_by('pk')
#         return render(request, "object_list.html", context={"objects": room_list, "columns": columns})


# class RoomCreateView(CreateView):
#     model = Room
#     fields = "__all__"
#     initial = {"name": "Nazwa1"}
#     template_name = "standard_create_view.html"
#     success_url = reverse_lazy("room_list")


# class ClientListView(LoginRequiredMixin, View):
#     def get(self, request):
#         columns = ["#", "Nazwisko", "Imię", "Data urodzenia", "Telefon", "e-mail", "Źródło", "Lider"]
#         client_list = Client.objects.all().order_by("last_name")
#         return render(request, "client_list_view.html", context={"objects": client_list, "columns": columns})

# ==================================== RESERVATION VIEWS ===============================================================
#
#
# class ReservationListView(View):
#     def get(self, request):
#         columns = ["#", "Zamawiający", "Kierunek", "Data rezerwacji"]
#         reservation_list = Reservation.objects.all().order_by('pk')
#         return render(request, "object_list.html", context={"objects": reservation_list, "columns": columns})
#
#
# class ReservationCreateView(CreateView):
#     form_class = ReservationCreateForm
#     template_name = "standard_create_view.html"
#     success_url = reverse_lazy("reservation_list")
#
#
# class ReservationDetailView(DetailView):
#     model = Reservation
#     template_name = "reservation_view.html"
#     columns = ["#", "Pokoj", "Cena", "Waluta", "Serwis",
#                "Data rezerwacji", "Data wyjazdu", "Data powrotu", "Klient"]
#     columns2 = ["#", "Pokoj", "Hotel", "Cena", "Waluta", "Data wyjazdu", "Data powrotu"]
#
#     def get_object(self, **kwargs):
#         id_ = self.kwargs.get("id")
#         return get_object_or_404(Reservation, id=id_)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({"columns": self.columns, "columns2": self.columns2})
#         return context
#
#
# class ReservationUpdateView(UpdateView):
#     model = Reservation
#     fields = ("owner", "price_service", "client")
#     template_name = "update_view.html"
#     success_url = reverse_lazy("reservation_list")
#
#     def get_object(self, **kwargs):
#         id_ = self.kwargs.get("id")
#         return get_object_or_404(Reservation, id=id_)
#
#
# class ReservationDeleteView(DeleteView):
#     model = Reservation
#     template_name = "delete_view.html"
#     success_url = reverse_lazy("reservation_list")
#
#     def get_object(self, **kwargs):
#         id_ = self.kwargs.get("id")
#         return get_object_or_404(Reservation, id=id_)


# ==================================== RESERVATION VIEWS ===============================================================


# class Reservation2ListView(ListView):
#     model = Reservation2
#     columns = [
#         "Data rezerwacji",
#         "Liczba nocy",
#         "Kraj",
#         "Region",
#         "Hotel",
#         "Liczba pokoi",
#         "Kategoria",
#         "Daty wyjazdu",
#         "Cena Offer",
#         "Waluta",
#         "Cena Net",
#         "Waluta",
#         "Kontrahent",
#     ]
#     ordering = ["date_of_reservation"]
#     template_name = "reservation/reservation_list_view.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(Reservation2ListView, self).get_context_data(**kwargs)
#         context['columns'] = self.columns
#         return context


# ==================================== ROOM RESERVATION VIEWS ==========================================================

# class RoomReservationCreateView(CreateView):
#     model = RoomReservation
#     fields = "__all__"
#     template_name = "standard_create_view.html"
#     success_url = reverse_lazy("reservation_list")
#
#
# class RoomReservationDeleteView(DeleteView):
#     model = RoomReservation
#     template_name = "delete_view.html"
#     success_url = reverse_lazy("reservation_list")
#
#     def get_object(self, **kwargs):
#         id_ = self.kwargs.get("id")
#         return get_object_or_404(RoomReservation, id=id_)

# class CreateContractView(View):
#     def get(self, request, id):
#         my_res = Reservation.objects.get(pk=id)
#         row = 46
#         my_xl = openpyxl.load_workbook("doc_patterns/instyle.xlsx")
#         my_xl["Sheet1"]["P21"].value = my_res.date_of_reservation
#         my_xl["Sheet1"]["P26"].value = f"{my_res.get_data[0]} - {my_res.get_data[1]}"
#         my_xl["Sheet1"]["B31"].value = f"{my_res.owner.first_name} {my_res.owner.last_name}"
#         my_xl["Sheet1"]["P31"].value = my_res.owner.date_of_birth
#         my_xl["Sheet1"]["B36"].value = \
#             f"{my_res.owner.postcode} {my_res.owner.city}\n{my_res.owner.address}"
#         my_xl["Sheet1"]["P36"].value = my_res.owner.phone_number
#         for participant in my_res.client.all():
#             my_xl["Sheet1"][f"B{row}"] = row - 45
#             my_xl["Sheet1"][f"C{row}"] = f"{participant.first_name} {participant.last_name}"
#             row += 1
#         row = 73
#         for room_reservation in RoomReservation.objects.filter(reservation_id=my_res.pk):
#             my_xl["Sheet1"][f"B{row}"].value = f'{room_reservation.room.hotel.country.name}, ' \
#                                                f'\n{room_reservation.room.hotel.region.name}'
#             my_xl["Sheet1"][f"F{row}"].value = f"{room_reservation.date_from} - {room_reservation.date_to}"
#             my_xl["Sheet1"][f"J{row}"].value = (room_reservation.date_to - room_reservation.date_from).days
#             my_xl["Sheet1"][f"L{row}"].value = room_reservation.room.hotel.name
#             my_xl["Sheet1"][f"R{row}"].value = "info o zakwaterowaniu"
#             my_xl["Sheet1"][f"W{row}"].value = "info o wyzywieniu"
#             row += 4
#         total_price = ""
#         for name, price in my_res.get_prices.items():
#             if total_price != "":
#                 total_price += " + "
#             total_price += f"{price} {name}"
#         my_xl["Sheet1"]["J131"].value = total_price
#         my_xl.save("doc_patterns/test.xlsx")
#         return render(request, "detail_view.html", context={"info": "Utworzono plik z umową!"})


# ==================================== FORMS ===========================================================================


# class ReservationCreateForm(forms.ModelForm):
#
#     def clean(self):
#         clean_data = super().clean()
#         if clean_data["price_service"] < 0:
#             raise ValidationError("Cena serwisu nie może być mniejsza niż 0")
#         return clean_data
#
#     class Meta:
#         model = Reservation
#         fields = ("owner", "price_service", "client")


# class RoomReservationCreateForm(forms.ModelForm):
#     class Meta:
#         model = RoomReservation
#         fields = "__all__"


# ==================================== URLS  ===========================================================================

# path("", reservation_views.ReservationListView.as_view(), name="reservation_list"),
# path("dodaj", reservation_views.ReservationCreateView.as_view(), name="reservation_create"),
# path("<int:id>", reservation_views.ReservationDetailView.as_view(), name="reservation_details"),
# path("<int:id>/edytuj", reservation_views.ReservationUpdateView.as_view(), name="reservation_update"),
# path("<int:id>/usun", reservation_views.ReservationDeleteView.as_view(), name="reservation_delete"),
# path("<int:id>/umowa", reservation_views.CreateContractView.as_view(), name="create_contract"),
#
# path("nowe", reservation_views.Reservation2ListView.as_view(), name="reservation_list_new"),
# path("usun_rez_pokoju/<int:id>/", reservation_views.RoomReservationDeleteView.as_view(), name="room_res_delete"),

# path("pokoje/", reservation_views.RoomListView.as_view(), name="room_list"),
# path("pokoje/dodaj", reservation_views.RoomCreateView.as_view(), name="room_create"),


# ======================================= CONTRACT_DETAIl_VIEW =========================================================
# {% extends "index.html" %}
# {% block content %}
#     <div class="row">
#         <div class="col-2">
#             Cena:
#         </div>
#         <div class="col-10">
#             {% for price in object.get_prices.items%}
#                 {{ price.1 }} {{ price.0 }}<br>
#             {% endfor %}
#         </div>
#     </div>
#     <div class="row">
#         <div class="col-2">
#             Cena za serwis:
#         </div>
#         <div class="col-10">
#             {{ object.price_service }} PLN
#         </div>
#     </div>
#     <div class="row">
#         <div class="col-2">
#             Data rezerwacji:
#         </div>
#         <div class="col-10">
#             {{ object.date_of_reservation|date:"Y-m-d" }}
#         </div>
#     </div>
#     <div class="row">
#         <div class="col-2">
#             Data wyjazdu:
#         </div>
#         <div class="col-10">
#             {{ object.get_dates.0|date:"Y-m-d" }}
#         </div>
#     </div>
#     <div class="row">
#         <div class="col-2">
#             Data powrotu:
#         </div>
#         <div class="col-10">
#             {{ object.get_dates.1|date:"Y-m-d" }}
#         </div>
#     </div>
#     <div class="row">
#         <div class="col-2">
#             Zamawiający:
#         </div>
#         <div class="col-10">
#             <a href="/reservation/klienci/{{ object.owner.id }}">{{ object.owner }}</a><br>
#         </div>
#     </div>
#     <div class="row">
#         <div class="col-2">
#             Uczestnicy:
#         </div>
#         <div class="col-10">
#             {% for client in object.client.all %}
#                 <a href="/reservation/klienci/{{ client.id }}">{{ client }}</a><br>
#             {% endfor %}
#         </div>
#     </div>
#     <table class="table table-striped">
#     <thead>
#         <tr>
#             {% for column in columns2 %}
#             <th scope="col">{{ column }}</th>
#             {% endfor %}
#             <th scope="col">Operacje</th>
#         </tr>
#     </thead>
#     <tbody>
#         {% for room_reservation in object.roomreservation_set.all %}
#         <tr>
#             <th scope="row">{{ room_reservation.id }}</th>
#             <td>
#                 {{ room_reservation.room }}
#             </td>
#             <td>
#                 {{ room_reservation.room.hotel }}
#             </td>
#             <td>
#                 {{ room_reservation.room.price }}
#     {#            {% for price in room_reservation.room.price %}#}
#     {#                {{ price }}#}
#     {#            {% endfor %}#}
#             </td>
#             <td>
#                 {{ room_reservation.room.currency.hash }}
#             </td>
#             <td>
#                 {{ room_reservation.date_from }}
#             </td>
#             <td>
#                 {{ room_reservation.date_to }}
#             </td>
#             <td>
#                 <a href="{{ room.get_delete_url}}" class="btn btn-info active" role="button" aria-pressed="true">Usuń</a>
#             </td>
#         </tr>
#         {% endfor %}
#     </tbody>
#     </table>
#         <div class="container">
#
#
#         <a href="/reservation/{{ object.id }}/zakwaterowanie" class="btn btn-info active" role="button" aria-pressed="true">Dodaj pokój</a>
#         <a href="{{ object.get_delete_url}}" class="btn btn-info active" role="button" aria-pressed="true">Usuń</a>
#         <a href="{{ object.id }}/umowa" class="btn btn-info active" role="button" aria-pressed="true">Twórz umowę</a>
#         </div>
# {% endblock %}
