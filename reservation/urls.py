from django.contrib import admin
from django.urls import path
from reservation import views

urlpatterns = [
    path("klienci/", views.ClientListView.as_view(), name="client_list"),
    path("klienci/dodaj", views.ClientCreateView.as_view(), name="client_create"),
    path("klienci/<int:id>", views.ClientDetailView.as_view(), name="client_details"),
    path("klienci/<int:id>/edytuj/", views.ClientUpdateView.as_view(), name="client_update"),
    path("klienci/<int:id>/usun/", views.ClientDeleteView.as_view(), name="client_delete"),

    path("hotele/", views.HotelListView.as_view(), name="hotel_list"),
    path("hotele/dodaj", views.HotelCreateView.as_view(), name="hotel_create"),
    path("hotele/<int:id>", views.HotelDetailView.as_view(), name="hotel_details"),
    path("hotele/<int:id>/edytuj", views.HotelUpdateView.as_view(), name="hotel_update"),
    path("hotele/<int:id>/usun", views.HotelDeleteView.as_view(), name="hotel_delete"),

]
