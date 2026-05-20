from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .forms import CarForm
from .models import Car

def home(request):
    cars = Car.objects.all()[:6]
    return render(request, 'Car_max/home.html', {'cars': cars})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'Car_max/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'Car_max/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    if not request.user.is_seller:
        return HttpResponseForbidden("No tienes permisos")

    cars = Car.objects.filter(owner=request.user)
    return render(request, 'Car_max/dashboard.html', {'cars': cars})

@login_required
def car_create(request):
    if not request.user.is_seller:
        return HttpResponseForbidden("Solo vendedores autorizados")

    form = CarForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        car = form.save(commit=False)
        car.owner = request.user
        car.save()
        form.save_m2m()
        return redirect('dashboard')

    return render(request, 'Car_max/car_form.html', {'form': form})

@login_required
def car_update(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if car.owner != request.user:
        return HttpResponseForbidden("No puedes editar este vehículo")

    form = CarForm(request.POST or None, request.FILES or None, instance=car)
    if form.is_valid():
        form.save()
        return redirect('dashboard')

    return render(request, 'Car_max/car_form.html', {'form': form})

@login_required
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if car.owner != request.user:
        return HttpResponseForbidden("No puedes eliminar este vehículo")

    if request.method == 'POST':
        car.delete()
        return redirect('dashboard')

    return render(request, 'Car_max/car_confirm_delete.html', {'car': car})