from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, View
from reservation.models import Client


class ClientCreateView(CreateView):
    model = Client
    fields = "__all__"
    success_url = reverse_lazy("list_client")
    template_name = "detail_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"info": "This is view for creating a new client"})
        return context


class ClientListView(View):
    def get(self, request):
        client_list = Client.objects.all()
        return render(request, "object_list.html", context={"objects": client_list})

