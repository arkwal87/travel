from django.urls import path
from reservation import views as reservation_views

urlpatterns = [
    path("klienci/", reservation_views.ClientListView.as_view(), name="client_list"),
    path("klienci/dodaj", reservation_views.ClientCreateView.as_view(), name="client_create"),
    path("klienci/<int:id>", reservation_views.ClientDetailView.as_view(), name="client_details"),
    path("klienci/<int:id>/edytuj/", reservation_views.ClientUpdateView.as_view(), name="client_update"),
    path("klienci/<int:id>/usun/", reservation_views.ClientDeleteView.as_view(), name="client_delete"),

    path("hotele/", reservation_views.HotelListView.as_view(), name="hotel_list"),
    path("hotele/dodaj", reservation_views.HotelCreateView.as_view(), name="hotel_create"),
    path("hotele/<int:id>", reservation_views.HotelDetailView.as_view(), name="hotel_details"),
    path("hotele/<int:id>/edytuj", reservation_views.HotelUpdateView.as_view(), name="hotel_update"),
    path("hotele/<int:id>/usun", reservation_views.HotelDeleteView.as_view(), name="hotel_delete"),
    path("hotele/<int:pk>/dodaj_pokoj", reservation_views.HotelRoomCreateView.as_view(), name="hotelroom_create"),

    path("pokoje/", reservation_views.RoomListView.as_view(), name="room_list"),
    path("pokoje/dodaj", reservation_views.RoomCreateView.as_view(), name="room_create"),
    path("pokoje/<int:id>", reservation_views.RoomDetailView.as_view(), name="room_details"),
    path("pokoje/<int:id>/edytuj", reservation_views.RoomUpdateView.as_view(), name="room_update"),
    path("pokoje/<int:id>/usun", reservation_views.RoomDeleteView.as_view(), name="room_delete"),

    path("reserwacje/", reservation_views.ReservationListView.as_view(), name="reservation_list"),
    path("dodaj", reservation_views.ReservationCreateView.as_view(), name="reservation_create"),
    path("rezerwacje/<int:id>", reservation_views.ReservationDetailView.as_view(), name="reservation_details"),
    path("rezerwacje/<int:id>/edytuj", reservation_views.ReservationUpdateView.as_view(), name="reservation_update"),
    path("rezerwacje/<int:id>/usun", reservation_views.ReservationDeleteView.as_view(), name="reservation_delete"),
    path("rezerwacje/<int:id>/umowa", reservation_views.CreateContractView.as_view(), name="create_contract"),

    path("rezerwacje/<int:id>/zakwaterowanie", reservation_views.RoomReservationCreateView.as_view(), name="room_res_create"),
    path("rezerwacje/usun_rez_pokoju/<int:id>/", reservation_views.RoomReservationDeleteView.as_view(), name="room_res_delete"),

    path('rest/get_countries/', reservation_views.get_countries_by_continent),
    path('rest/get_regions/', reservation_views.get_regions_by_countries),

]
