from django.contrib import admin
from .models import Client, Hotel, Reference, Country, Continent, Region, RoomCategory, Currency, MealPlan, \
    Counterparty, ContractRoom, Contract, Room, Villa


# Register your models here.
admin.site.register(Client)
admin.site.register(Hotel)
admin.site.register(Reference)
admin.site.register(Country)
admin.site.register(Continent)
admin.site.register(Region)
admin.site.register(RoomCategory)
admin.site.register(Currency)
admin.site.register(MealPlan)
admin.site.register(Counterparty)
admin.site.register(ContractRoom)
admin.site.register(Contract)
admin.site.register(Room)
admin.site.register(Villa)