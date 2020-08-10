from django.contrib import admin
from django.urls import path
from reservation import views

urlpatterns = [
    path("klienci/", views.ClientListView.as_view(), name="client_list"),
    path("klienci/dodaj", views.ClientCreateView.as_view(), name="client_create"),
    path("klienci/<int:id>", views.ClientDetailView.as_view(), name="client_details"),
    path("klienci/<int:id>/edytuj/", views.ClientUpdateView.as_view(), name="client_update"),
    path("klienci/<int:id>/usun/", views.ClientDeleteView.as_view(), name="client_delete"),

]
