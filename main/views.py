from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import RegistrationForm, CustomLoginForm, MaterialForm
from .models import Material


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


@login_required
def material_list(request):
    query = request.GET.get("q")
    materials = Material.objects.all()
    if query:
        materials = materials.filter(name__icontains=query)
    return render(request, "material_list.html", {"materials": materials})


@login_required
def material_create(request):
    if request.method == "POST":
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("material_list")
    else:
        form = MaterialForm()
    return render(request, "material_form.html", {"form": form, "title": "Добавить материал"})


@login_required
def material_edit(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == "POST":
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect("material_list")
    else:
        form = MaterialForm(instance=material)
    return render(request, "material_form.html", {"form": form, "title": "Редактировать материал"})


@login_required
def material_delete(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == "POST":
        material.delete()
        return redirect("material_list")
    return render(request, "material_confirm_delete.html", {"material": material})