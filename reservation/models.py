from django.db import models

# Create your models here.
from django.db.models import Sum


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


class Payment(models.Model):
    reservation_no = models.ForeignKey("Reservation", on_delete=models.SET_NULL, null=True)
    paid = models.BooleanField(default=False)


class Client(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=9, null=True)
    email = models.EmailField(null=True)
    city = models.CharField(max_length=32, null=True)
    postcode = models.CharField(max_length=6, null=True)
    address = models.TextField(null=True)

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
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
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


class RoomReservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    date_from = models.DateField()
    date_to = models.DateField()
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    def get_delete_url(self):
        return f"/reservation/usun_rez_pokoju/{self.pk}/"


class Reservation(models.Model):
    price_service = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    date_of_reservation = models.DateField(auto_now_add=True, blank=True)
    client = models.ManyToManyField(Client, related_name="reservation_set")
    owner = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="reservation_owner", null=True)

    def __str__(self):
        return f"Numer {self.pk}"

    @property
    def get_data(self):
        if RoomReservation.objects.filter(reservation=self).exists():
            date_from = RoomReservation.objects.filter(reservation=self).order_by("date_from").first().date_from
            date_to = RoomReservation.objects.filter(reservation=self).order_by("date_to").last().date_to
            # total_sum = RoomReservation.objects.filter(reservation=self).aggregate(Sum('price'))["price__sum"]
            return [date_from, date_to]

    @property
    def get_prices(self):
        all_prices = {}
        for room_res in RoomReservation.objects.filter(reservation=self):
            if room_res.room.currency.hash in all_prices:
                all_prices[room_res.room.currency.hash] += room_res.room.price
            else:
                all_prices[room_res.room.currency.hash] = room_res.room.price
        return all_prices

    def get_detail_url(self):
        return f"/reservation/{self.pk}"

    def get_update_url(self):
        return f"/reservation/{self.pk}/edytuj"

    def get_delete_url(self):
        return f"/reservation/{self.pk}/usun"

    def get_unique_regions(self):
        regions = []
        for i in RoomReservation.objects.filter(reservation=self).distinct("room"):
            if i.room.hotel.region not in regions:
                regions.append(i.room.hotel.region)
        return regions
