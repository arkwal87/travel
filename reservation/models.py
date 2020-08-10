from django.db import models


# Create your models here.

class Continent(models.Model):
    name = models.CharField(max_length=32)
    hash = models.CharField(max_length=6)


class Country(models.Model):
    name = models.CharField(max_length=32)
    hash = models.CharField(max_length=6)


class Region(models.Model):
    name = models.CharField(max_length=32)
    hash = models.CharField(max_length=6)


class Currency(models.Model):
    name = models.CharField(max_length=32)
    symbol = models.CharField(max_length=1)
    hash = models.CharField(max_length=4)
    rate = models.FloatField()


class Client(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=9, null=True)
    email = models.EmailField(null=True)


class Hotel(models.Model):
    name = models.CharField(max_length=32)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Room(models.Model):
    name = models.CharField(max_length=32)
    price = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True)


class Payment(models.Model):
    reservation_no = models.ForeignKey("Reservation", on_delete=models.SET_NULL, null=True)
    paid = models.BooleanField(default=False)


class Reservation(models.Model):
    price = models.DecimalField(decimal_places=4, max_digits=5)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    price_service = models.DecimalField(decimal_places=2, max_digits=5)
    date_of_reservation = models.DateField(auto_now_add=True, blank=True)
    date_from = models.DateField()
    date_to = models.DateField()
    paid = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    client = models.ManyToManyField(Client)

