from django.urls import path
from reservation import views as reservation_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("klienci/", reservation_views.ClientListView.as_view(), name="client_list"),
    path("klienci/dodaj", reservation_views.ClientCreateView.as_view(), name="client_create"),
    path("klienci/<int:id>", reservation_views.ClientDetailView.as_view(), name="client_details"),
    path("klienci/<int:id>/edytuj/", reservation_views.ClientUpdateView.as_view(), name="client_update"),
    path("klienci/<int:id>/usun/", reservation_views.ClientDeleteView.as_view(), name="client_delete"),

    path("hotele/", reservation_views.HotelListView.as_view(), name="hotel_list"),
    path("hotele/dodaj/", reservation_views.HotelCreateView.as_view(), name="hotel_create"),
    path("hotele/<int:id>/", reservation_views.HotelDetailView.as_view(), name="hotel_details"),
    path("hotele/<int:id>/edytuj/", reservation_views.HotelUpdateView.as_view(), name="hotel_update"),
    path("hotele/<int:id>/usun/", reservation_views.HotelDeleteView.as_view(), name="hotel_delete"),
    path("hotele/<int:pk>/dodaj_pokoj/", reservation_views.HotelRoomCreateView.as_view(), name="hotelroom_create"),

    path("wille/", reservation_views.VillaListView.as_view(), name="villa_list"),
    path("wille/dodaj", reservation_views.VillaCreateView.as_view(), name="villa_create"),
    path("wille/<int:id>", reservation_views.VillaDetailView.as_view(), name="villa_details"),
    path("wille/<int:id>/edytuj", reservation_views.VillaUpdateView.as_view(), name="villa_update"),
    path("wille/<int:id>/usun", reservation_views.VillaDeleteView.as_view(), name="villa_delete"),

    path("pociagi/", reservation_views.TrainListView.as_view(), name="train_list"),
    path("pociagi/dodaj", reservation_views.TrainCreateView.as_view(), name="train_create"),
    path("pociagi/<int:id>", reservation_views.TrainDetailView.as_view(), name="train_details"),
    path("pociagi/<int:id>/edytuj", reservation_views.TrainUpdateView.as_view(), name="train_update"),
    path("pociagi/<int:id>/usun", reservation_views.TrainDeleteView.as_view(), name="train_delete"),

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
    path("umowy/<int:id>/usun", reservation_views.ContractDeleteView.as_view(), name="contract_delete"),
    path("umowy/<int:id>/umowa", reservation_views.CreateContractView.as_view(), name="create_contract"),
    path("umowy/<int:id>/downloadfile/", reservation_views.downloadFile, name='downloadfile'),
    path("umowy/<int:id>/download/", reservation_views.downloadPdf, name='download'),
    path("umowy/<int:id>/uploadfile/", reservation_views.UploadView.as_view(), name='uploadfile'),

    path("umowy/<int:id>/wplata/", reservation_views.PaymentCreateView.as_view(), name='payment_create'),
    path("umowy/<int:id>/wplata/<int:pk>/edytuj", reservation_views.PaymentUpdateView.as_view(), name='payment_update'),
    path("umowy/<int:id>/wplata/<int:pk>/usun", reservation_views.PaymentDeleteView.as_view(), name='payment_delete'),

    path("umowy/<int:id>/pokoj/",
         reservation_views.ContractRoomCreateView.as_view(),
         name="contract_room_create"),
    path("umowy/<int:id>/pokoj/<int:pk>/edytuj/",
         reservation_views.ContractRoomUpdateView.as_view(),
         name="contract_room_update"),
    path("umowy/<int:id>/pokoj/<int:pk>/usun/",
         reservation_views.ContractRoomDeleteView.as_view(),
         name="contract_room_delete"),

    path("umowy/<int:id>/willa/",
         reservation_views.ContractVillaCreateView.as_view(),
         name="contract_villa_create"),
    path("umowy/<int:id>/willa/<int:pk>/edytuj/",
         reservation_views.ContractVillaUpdateView.as_view(),
         name="contract_villa_update"),
    path("umowy/<int:id>/willa/<int:pk>/usun/",
         reservation_views.ContractVillaDeleteView.as_view(),
         name="contract_villa_delete"),

    path("umowy/<int:id>/pociag/",
         reservation_views.ContractTrainCreateView.as_view(),
         name="contract_train_create"),
    path("umowy/<int:id>/pociag/<int:pk>/edytuj/",
         reservation_views.ContractTrainUpdateView.as_view(),
         name="contract_train_update"),
    path("umowy/<int:id>/pociag/<int:pk>/usun/",
         reservation_views.ContractTrainDeleteView.as_view(),
         name="contract_train_delete"),

    path("umowy/<int:id>/ubezpieczenie/",
         reservation_views.ContractInsuranceCreateView.as_view(),
         name="contract_insurance_create"),
    path("umowy/<int:id>/ubezpieczenie/<int:pk>/edytuj/",
         reservation_views.ContractInsuranceUpdateView.as_view(),
         name="contract_insurance_update"),
    path("umowy/<int:id>/ubezpieczenie/<int:pk>/usun/",
         reservation_views.ContractInsuranceDeleteView.as_view(),
         name="contract_insurance_delete"),

    path("umowy/<int:id>/bilet/",
         reservation_views.ContractTicketCreateView.as_view(),
         name="contract_ticket_create"),
    path("umowy/<int:id>/bilet/<int:pk>/edytuj/",
         reservation_views.ContractTicketUpdateView.as_view(),
         name="contract_ticket_update"),
    path("umowy/<int:id>/bilet/<int:pk>/usun/",
         reservation_views.ContractTicketDeleteView.as_view(),
         name="contract_ticket_delete"),
    path("umowy/<int:id>/bilet/<int:pk>/",
         reservation_views.ContractTicketDetailView.as_view(),
         name="contract_ticket_details"),

    path("umowy/<int:id>/inne/",
         reservation_views.ContractOtherCreateView.as_view(),
         name="contract_other_create"),
    path("umowy/<int:id>/inne/<int:pk>/edytuj/",
         reservation_views.ContractOtherUpdateView.as_view(),
         name="contract_other_update"),
    path("umowy/<int:id>/inne/<int:pk>/usun/",
         reservation_views.ContractOtherDeleteView.as_view(),
         name="contract_other_delete"),
    path("umowy/<int:id>/inne/<int:pk>/",
         reservation_views.ContractOtherDetailView.as_view(),
         name="contract_other_details"),

    path("upload/", reservation_views.upload, name="upload_file"),

    # path("downloadfile2/", reservation_views.DownloadView, name='downloadfile2'),

    # path('excel/', views1.downloadexcel, name="downloadexcel"),

    path('rest/get_countries/', reservation_views.get_countries_by_continent),
    path('rest/get_regions/', reservation_views.get_regions_by_countries),
    path('rest/get_hotels/', reservation_views.get_hotels_by_regions),
    path('rest/get_villas/', reservation_views.get_villas_by_regions),
    path('rest/get_rooms/', reservation_views.get_rooms_by_hotels),

    path('rest/datatables_lang/', reservation_views.datatables_lang),

    path('test/', reservation_views.populate_db, name="test_view_db")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
