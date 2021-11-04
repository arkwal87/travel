from django.db import models
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

    # def get_create_url(self):
    #     return "/reservation/kontrahenci/dodaj"


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


class Client(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=9, null=True)
    email = models.EmailField(null=True)
    city = models.CharField(max_length=32, null=True)
    postcode = models.CharField(max_length=6, null=True)
    address = models.TextField(null=True)
    leader = models.BooleanField(default=False)
    reference = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_detail_url(self):
        return f"/reservation/klienci/{self.pk}"

    def get_update_url(self):
        return f"/reservation/klienci/{self.pk}/edytuj"

    def get_delete_url(self):
        return f"/reservation/klienci/{self.pk}/usun"

    # def get_create_url(self):
    #     return "/reservation/klienci/dodaj"


class Hotel(models.Model):
    name = models.CharField(max_length=32)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    link = models.CharField(max_length=128, default="", blank=True, null=True)

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
    # price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
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
    pool = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.region}'

    def get_detail_url(self):
        return f"/reservation/wille/{self.pk}"

    def get_update_url(self):
        return f"/reservation/wille/{self.pk}/edytuj"

    def get_delete_url(self):
        return f"/reservation/wille/{self.pk}/usun"


class RoomCategory(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Message(models.Model):
    date_of_message = models.DateField(auto_now_add=True, blank=True)
    message_text = models.TextField()


class Contract(models.Model):
    date_of_contract = models.DateField()
    client = models.ManyToManyField(Client)
    owner = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="contract_owner")

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
        if ContractRoom.objects.filter(contract=self).exists():
            date_from = ContractRoom.objects.filter(contract=self).order_by("date_from").first().date_from
            date_to = ContractRoom.objects.filter(contract=self).order_by("date_to").last().date_to
            return [date_from, date_to]


class ContractRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    date_from = models.DateField()
    date_to = models.DateField()
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)
    # room_category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    room_number = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
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
