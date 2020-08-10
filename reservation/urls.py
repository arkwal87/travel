from django.contrib import admin
from django.urls import path
from reservation import views

urlpatterns = [
    path("klienci/dodaj", views.ClientCreateView.as_view(), name="create_client"),
    path("klienci/usun/<int:id>", views.ClientDeleteView.as_view(), name="delete_client"),
    path("klienci/", views.ClientListView.as_view(), name="list_client")

]
