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

    path("wille/", reservation_views.VillaListView.as_view(), name="villa_list"),
    path("wille/dodaj", reservation_views.VillaCreateView.as_view(), name="villa_create"),
    path("wille/<int:id>", reservation_views.VillaDetailView.as_view(), name="villa_create"),

    path("pokoje/<int:id>", reservation_views.RoomDetailView.as_view(), name="room_details"),
    path("pokoje/<int:id>/edytuj", reservation_views.RoomUpdateView.as_view(), name="room_update"),
    path("pokoje/<int:id>/usun", reservation_views.RoomDeleteView.as_view(), name="room_delete"),

    path("kontrahenci/", reservation_views.CounterpartyListView.as_view(), name="counterparty_list"),
    path("kontrahenci/dodaj", reservation_views.CounterpartyCreateView.as_view(), name="counterparty_create"),
    path("kontrahenci/<int:id>", reservation_views.CounterpartyDetailView.as_view(), name="counterparty_details"),
    path("kontrahenci/<int:id>/edytuj", reservation_views.CounterpartyUpdateView.as_view(), name="counterparty_update"),
    path("kontrahenci/<int:id>/usun", reservation_views.CounterpartyDeleteView.as_view(), name="counterparty_delete"),

    path("umowy/", reservation_views.ContractListView.as_view(), name="contract_list"),
    path("umowy/dodaj", reservation_views.ContractCreateView.as_view(), name="contract_create"),
    path("umowy/<int:id>", reservation_views.ContractDetailView.as_view(), name="contract_detail_view"),
    path("umowy/<int:id>/edytuj", reservation_views.ContractUpdateView.as_view(), name="contract_update"),

    path("<int:id>/zakwaterowanie", reservation_views.ContractRoomCreateView.as_view(), name="contract_room_create"),
    path("<int:id>/zawillowanie", reservation_views.ContractRoomCreateView.as_view(), name="contract_prod_create"),

    path('rest/get_countries/', reservation_views.get_countries_by_continent),
    path('rest/get_regions/', reservation_views.get_regions_by_countries),
    path('rest/get_hotels/', reservation_views.get_hotels_by_regions),
    path('rest/get_rooms/', reservation_views.get_rooms_by_hotels),

    path('rest/datatables_lang/', reservation_views.datatables_lang),

    path('test/', reservation_views.populate_db, name="test_view_db")

]
