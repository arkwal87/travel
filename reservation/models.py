from django.db import models
from django.db.models import Sum
from django.core.validators import MinValueValidator


class MealPlan(models.Model):
    name = models.CharField(max_length=32)
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return self.short_name


class Counterparty(models.Model):
    short_name = models.CharField(max_length=16)
    full_name = models.CharField(max_length=128)
    VAT_no = models.CharField(max_length=10)
    country = models.CharField(max_length=16)
    post_code = models.CharField(max_length=10)
    city = models.CharField(max_length=32)
    address = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.short_name}"

    def get_detail_url(self):
        return f"/reservation/kontrahenci/{self.pk}"

    def get_update_url(self):
        return f"/reservation/kontrahenci/{self.pk}/edytuj"

    def get_delete_url(self):
        return f"/reservation/kontrahenci/{self.pk}/usun"


class Reference(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Continent(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=32)
    continent = models.ForeignKey(Continent, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=32)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=32)
    hash = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=5, decimal_places=4)

    def __str__(self):
        return self.hash


class BankAccount(models.Model):
    currency_hash = models.ForeignKey(Currency, on_delete=models.CASCADE)
    account_no = models.CharField(max_length=26)

    def __str__(self):
        return f"Rachunek w {self.currency_hash}"


class Client(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=9, null=True)
    email = models.EmailField(null=True)
    city = models.CharField(max_length=32, null=True)
    postcode = models.CharField(max_length=6, null=True)
    address = models.TextField(null=True)
    reference = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_detail_url(self):
        return f"/reservation/klienci/{self.pk}"

    def get_update_url(self):
        return f"/reservation/klienci/{self.pk}/edytuj"

    def get_delete_url(self):
        return f"/reservation/klienci/{self.pk}/usun"


class Hotel(models.Model):
    name = models.CharField(max_length=32)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    link = models.CharField(max_length=128, default="", blank=True, null=True)
    category = models.CharField(
        choices=[
            ('-', "-"),
            ('*', "*"),
            ('**', "**"),
            ('***', "***"),
            ('****', "****"),
            ('*****', "*****")],
        default="*",
        max_length=5)

    def __str__(self):
        return f'{self.name} - {self.region}'

    def get_detail_url(self):
        return f"/reservation/hotele/{self.pk}"

    def get_update_url(self):
        return f"/reservation/hotele/{self.pk}/edytuj"

    def get_delete_url(self):
        return f"/reservation/hotele/{self.pk}/usun"


class Room(models.Model):
    name = models.CharField(max_length=32)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True)
    room_size = models.IntegerField(null=True)
    terrace_size = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    def get_detail_url(self):
        return f"/reservation/pokoje/{self.pk}"

    def get_update_url(self):
        return f"/reservation/pokoje/{self.pk}/edytuj"

    def get_delete_url(self):
        return f"/reservation/pokoje/{self.pk}/usun"


class Villa(models.Model):
    name = models.CharField(max_length=32)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    link = models.CharField(max_length=128, default="", blank=True, null=True)
    size = models.IntegerField(null=True)
    rooms_no = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.name} - {self.region}'

    def get_detail_url(self):
        return f"/reservation/wille/{self.pk}"

    def get_update_url(self):
        return f"/reservation/wille/{self.pk}/edytuj"

    def get_delete_url(self):
        return f"/reservation/wille/{self.pk}/usun"


class Train(models.Model):
    name = models.CharField(max_length=32, verbose_name='Nazwa')
    dest_from = models.CharField(max_length=128, default="", blank=True, null=True, verbose_name='Miasto początkowe')
    dest_to = models.CharField(max_length=128, default="", blank=True, null=True, verbose_name='Miasto docelowe')

    def __str__(self):
        return f'{self.name}'

    def get_detail_url(self):
        return f"/reservation/pociagi/{self.pk}"

    def get_update_url(self):
        return f"/reservation/pociagi/{self.pk}/edytuj"

    def get_delete_url(self):
        return f"/reservation/pociagi/{self.pk}/usun"


class Airline(models.Model):
    name = models.CharField(max_length=32)
    link = models.CharField(max_length=128, default="", blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


# class Airport(models.Model):
#     name = models.CharField(max_length=32)
#     city = models.CharField(max_length=32)
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)
#     short_name = models.CharField(max_length=8)


# class AirplaneRoutes(models.Model):
#     departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="dep_airport")
#     arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arr_dest")
#     departure_date = models.DateField()
#     arrival_date = models.DateField()


class Message(models.Model):
    date_of_message = models.DateField(auto_now_add=True, blank=True)
    message_text = models.TextField()


class Contract(models.Model):
    name = models.CharField(max_length=14, blank=True, editable=False)
    date_of_contract = models.DateField(auto_now_add=True, null=True, blank=True)
    date_of_sign = models.DateField(null=True, blank=True)
    client = models.ManyToManyField(Client)
    owner = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="contract_owner")
    leader = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="contract_leader")
    # TUTAJ ZMIEN NULL I BLANK! MUSI BYC PODANE!
    payment_deadline = models.DateField(null=True, blank=True)
    cancellation_deadline = models.DateField(null=True, blank=True)
    cancellation_policy = models.TextField(null=True, blank=True)
    payment_policy = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def get_detail_url(self):
        return f"/reservation/umowy/{self.pk}"

    def get_update_url(self):
        return f"/reservation/umowy/{self.pk}/edytuj"

    def get_delete_url(self):
        return f"/reservation/umowy/{self.pk}/usun"

    @property
    def get_dates(self):
        dates_from = []
        dates_to = []
        if ContractRoom.objects.filter(contract=self).exists():
            dates_from.append(ContractRoom.objects.filter(contract=self).order_by("date_from").first().date_from)
            dates_to.append(ContractRoom.objects.filter(contract=self).order_by("date_to").last().date_to)
        if ContractVilla.objects.filter(contract=self).exists():
            dates_from.append(ContractVilla.objects.filter(contract=self).order_by("date_from").first().date_from)
            dates_to.append(ContractVilla.objects.filter(contract=self).order_by("date_to").last().date_to)
        if not dates_from:
            dates_from = [0]
        if not dates_to:
            dates_to = [0]
        return [min(dates_from), max(dates_to)]

    def get_price_dict(self):
        final_res = {}
        products = ["Pokoje", "Wille", "Pociągi", "Bilety", "Ubezpieczenia", "Inne"]
        for index, model in enumerate([ContractRoom, ContractVilla, ContractTrain, ContractTicket, ContractInsurance,
                                       ContractOther]):
            if self.get_prices(model_name=model) != {}:
                final_res[products[index]] = self.get_prices(model_name=model)
        return final_res

    def get_all_prices(self):
        models_list = [ContractRoom, ContractVilla, ContractTrain, ContractInsurance, ContractTicket, ContractOther]
        price_sum = {}
        for model_name in models_list:
            model_sum = self.get_prices(model_name)
            price_sum = {
                k: float(0 if model_sum.get(k, 0) is None else model_sum.get(k, 0)) +
                   float(0 if price_sum.get(k, 0) is None else price_sum.get(k, 0))
                for k in set(model_sum) | set(price_sum)
            }
        return price_sum

    def get_prices(self, model_name):
        price_results = {}
        for currency in Currency.objects.all():
            cur_value = model_name.objects.filter(
                contract=self, offer_currency=currency
            ).aggregate(Sum("price_offer"))['price_offer__sum']
            if cur_value is not None:
                price_results[currency.hash] = cur_value
        return price_results


class ContractFile(models.Model):
    file_name = models.CharField(max_length=100)
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)
    pdf = models.FileField(upload_to="pdfs")

    def __str__(self):
        return self.file_name


class ContractRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    date_from = models.DateField()
    date_to = models.DateField()
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)
    room_number = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    # offer - dla klienta
    price_offer = models.DecimalField(max_digits=10, decimal_places=2)
    price_net = models.DecimalField(max_digits=10, decimal_places=2)
    offer_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="offer_room_currency")
    net_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="net_room_currency")
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE)
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)


class ContractVilla(models.Model):
    villa = models.ForeignKey(Villa, on_delete=models.SET_NULL, null=True)
    date_from = models.DateField()
    date_to = models.DateField()
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)
    price_offer = models.DecimalField(max_digits=10, decimal_places=2)
    price_net = models.DecimalField(max_digits=10, decimal_places=2)
    offer_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="offer_villa_currency")
    net_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="net_villa_currency")
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE)
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)


class ContractTrain(models.Model):
    train = models.ForeignKey(Train, on_delete=models.SET_NULL, null=True)
    cabin_name = models.CharField(max_length=32)
    date_from = models.DateField()
    date_to = models.DateField()
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)
    price_offer = models.DecimalField(max_digits=10, decimal_places=2)
    price_net = models.DecimalField(max_digits=10, decimal_places=2)
    offer_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="offer_train_currency")
    net_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="net_train_currency")
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE)
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)


class ContractOther(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    date_from = models.DateField()
    date_to = models.DateField()
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)
    price_offer = models.DecimalField(max_digits=10, decimal_places=2)
    price_net = models.DecimalField(max_digits=10, decimal_places=2)
    offer_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="offer_product_currency")
    net_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="net_product_currency")
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE)


class ContractInsurance(models.Model):
    type = models.IntegerField(choices=[(1, "Podróżne"), (2, "Kosztów rezygnacji")], default=1)
    insurance_no = models.CharField(max_length=256)
    price_offer = models.DecimalField(max_digits=10, decimal_places=2)
    price_net = models.DecimalField(max_digits=10, decimal_places=2)
    offer_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="offer_insurance_currency")
    net_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="net_insurance_currency")
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)
    extra_notes = models.TextField(null=True)


class ContractTicket(models.Model):
    ticket_class = models.IntegerField(choices=[(1, "Ekonomiczna"), (2, "Biznesowa"), (3, "Pierwsza")], default=1)
    airline = models.ForeignKey(Airline, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    # TUTAJ ZMIEN NULL I BLANK! MUSI BYC PODANE!
    date_departure = models.DateField(null=True, blank=True)
    date_arrival = models.DateField(null=True, blank=True)
    price_offer = models.DecimalField(max_digits=10, decimal_places=2)
    price_net = models.DecimalField(max_digits=10, decimal_places=2)
    offer_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="offer_ticket_currency")
    net_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="net_ticket_currency")
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)
    ticket_details = models.TextField(null=True, blank=True)
    extra_notes = models.TextField(null=True, blank=True)


class Payment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    payment_date = models.DateField()


# class Ticket(models.Model):
#     kierunek = models.ForeignKey(AirplaneRoutes, on_delete=models.SET_NULL, null=True)
#     klasa = models.CharField(max_length=32)
#     airline = models.ForeignKey(Airline, on_delete=models.SET_NULL, null=True)
#     pasazer = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
#     price_offer = models.DecimalField(max_digits=10, decimal_places=2)
#     price_net = models.DecimalField(max_digits=10, decimal_places=2)
#     offer_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="offer_ticket")
#     net_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="net_ticket")
#
#
# class ContractAirplaneRoutes(models.Model):
#     trasa = models.ForeignKey(AirplaneRoutes, on_delete=models.SET_NULL, null=True)
#
#
# class ContractTicketOLD2(models.Model):
#     bilet = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True)
#     trasy = models.ForeignKey(ContractAirplaneRoutes, on_delete=models.SET_NULL, null=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#
#
# class ContractTicketOLD(models.Model):
#     name = models.CharField(max_length=32)
#     price_offer = models.DecimalField(max_digits=10, decimal_places=2)
#     price_net = models.DecimalField(max_digits=10, decimal_places=2)
#     offer_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="offer_ticket_currency")
#     net_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="net_ticket_currency")
#     counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE)
#     # airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
#     # flight_class = models.CharField(max_length=32)
#     quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
#     contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)


# class ContractTest(models.Model):
#     room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
#     villa = models.ForeignKey(Villa, on_delete=models.SET_NULL, null=True)
#     date_from = models.DateField()
#     date_to = models.DateField()
#     contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=False)
#     price_offer = models.DecimalField(max_digits=10, decimal_places=2)
#     price_net = models.DecimalField(max_digits=10, decimal_places=2)
#     offer_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="offer_room_currency")
#     net_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="net_room_currency")
#     counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE, null=False)
#     meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, null=True)
#     quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], null=True)
#     airline = models.ForeignKey(Airline, on_delete=models.CASCADE, null=True)
#     flight_class = models.CharField(max_length=32, null=True)
#     description = models.CharField(max_length=256, null=True)
#     cabin_category = models.CharField(max_length=32, null=True)
