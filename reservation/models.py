from django.db import models


# Create your models here.

class Continent(models.Model):
    name = models.CharField(max_length=32)
    hash = models.CharField(max_length=6)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=32)
    hash = models.CharField(max_length=6)
    continent = models.ForeignKey(Continent, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=32)
    hash = models.CharField(max_length=6)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=32)
    hash = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=5, decimal_places=4)

    def __str__(self):
        return self.name


# ======================================================================================================================

#
# class ClientReservation(models.Model):
#     client = models.ForeignKey("Client", on_delete=models.CASCADE)
#     reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)


# =======================================================================================================================


class Client(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=9, null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_detail_url(self):
        return f"/reservation/klienci/{self.pk}"

    def get_update_url(self):
        return f"/reservation/klienci/{self.pk}/edytuj"

    def get_delete_url(self):
        return f"/reservation/klienci/{self.pk}/usun"

    def get_create_url(self):
        return "/reservation/klienci/dodaj"


class Hotel(models.Model):
    name = models.CharField(max_length=32)
    continent = models.ForeignKey(Continent, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    link = models.CharField(max_length=128, default="")

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
    price = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_detail_url(self):
        return f"/reservation/pokoje/{self.pk}"

    def get_update_url(self):
        return f"/reservation/pokoje/{self.pk}/edytuj"

    def get_delete_url(self):
        return f"/reservation/pokoje/{self.pk}/usun"


class Payment(models.Model):
    reservation_no = models.ForeignKey("Reservation", on_delete=models.SET_NULL, null=True)
    paid = models.BooleanField(default=False)


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    price_service = models.DecimalField(decimal_places=2, max_digits=10)
    date_of_reservation = models.DateField(auto_now_add=True, blank=True)
    date_from = models.DateField()
    date_to = models.DateField()
    client = models.ManyToManyField(Client)

    def __str__(self):
        return f"Numer {self.pk}"

    @property
    def currency_conversion(self):
        return round(self.price * self.currency.rate,2)

    def get_detail_url(self):
        return f"/reservation/{self.pk}"

    def get_update_url(self):
        return f"/reservation/{self.pk}/edytuj"

    def get_delete_url(self):
        return f"/reservation/{self.pk}/usun"

