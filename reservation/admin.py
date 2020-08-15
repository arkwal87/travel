from django.contrib import admin
from .models import Reservation, Client

# Register your models here.

admin.site.register(Reservation)
admin.site.register(Client)