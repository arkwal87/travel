from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
# class RegisterView(View):
#     def get(self, request):
#         form = UserCreationForm()
#         return render(request, "users/register.html", context={"form": form})
#
#     def post(self, request):
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             messages.success(request, f"Stworzono użytkownika {username}")
#             # return redirect("style_main_page")
#             return render(request, "users/register.html", context={"form": form})

def RegisterView(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Twoje konto zostało stworzone. Możesz się zalogować")
            return redirect("login")
    else:
        form = UserRegistrationForm()
        return render(request, "users/register.html", context={"form": form})


@login_required
def ProfileView(request):
    return render(request, "users/profile.html")
