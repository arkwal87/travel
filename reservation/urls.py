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

    path("pokoje/", views.RoomListView.as_view(), name="room_list"),
    path("pokoje/dodaj", views.RoomCreateView.as_view(), name="room_create"),
    path("pokoje/<int:id>", views.RoomDetailView.as_view(), name="room_details"),
    path("pokoje/<int:id>/edytuj", views.RoomUpdateView.as_view(), name="room_update"),
    path("pokoje/<int:id>/usun", views.RoomDeleteView.as_view(), name="room_delete"),

    path("", views.ReservationListView.as_view(), name="reservation_list"),
    path("dodaj", views.ReservationCreateView.as_view(), name="reservation_create"),
    path("<int:id>", views.ReservationDetailView.as_view(), name="reservation_details"),
    path("<int:id>/edytuj", views.ReservationUpdateView.as_view(), name="reservation_update"),
    path("<int:id>/usun", views.ReservationDeleteView.as_view(), name="reservation_delete"),
    path("<int:id>/umowa", views.CreateContractView.as_view(), name="create_contract"),
    
    path("<int:id>/dodaj_pokoj", views.RoomReservationCreateView.as_view(), name="room_res_create"),
    path("usun_rez_pokoju/<int:id>/", views.RoomReservationDeleteView.as_view(), name="room_res_delete"),

]
