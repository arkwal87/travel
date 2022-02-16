from django.contrib import admin
from .models import Client, Hotel, Reference, Country, Continent, Region, Currency, MealPlan, Counterparty, \
    ContractRoom, Contract, Room, Villa, Train, ContractVilla, BankAccount

# Register your models here.
admin.site.register(Client)
admin.site.register(Hotel)
admin.site.register(Reference)
admin.site.register(Country)
admin.site.register(Continent)
admin.site.register(Region)
admin.site.register(Currency)
admin.site.register(MealPlan)
admin.site.register(Counterparty)
admin.site.register(ContractRoom)
admin.site.register(Contract)
admin.site.register(Room)
admin.site.register(Villa)
admin.site.register(Train)
admin.site.register(ContractVilla)
admin.site.register(BankAccount)