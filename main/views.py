from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegistrationForm, CustomLoginForm


def home(request):
  return render(request, 'home.html', {})


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # сразу авторизуем
            return redirect("home")
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})


def logout_action(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('home', permanent=False)


def custom_login(request):
    error = None

    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                error = "Неверное имя пользователя или пароль."
    else:
        form = CustomLoginForm()

    return render(request, "custom_login.html", {"form": form, "error": error})


