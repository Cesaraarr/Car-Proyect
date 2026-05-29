# 🚀 SPRINT 1 — Setup + Modelado Base

## 🎯 Objetivo

Tener:
* Proyecto Django funcionando
* App store (tienda)
* Modelos con relaciones:
    * 1:N → Usuario → Producto
    * N:M → Producto ↔ Categoría
    * N:M → Carrito ↔ Producto (con CartItem)
* Admin operativo

## 1 Crear proyecto en django

```bash
django-admin startproject marketplace_main
cd marketplace_main
python manage.py startapp store
2 Configurar settings.py
📌 Agregar app

Python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Car_max'
]
📌 Usuario personalizado

Python
AUTH_USER_MODEL = 'Car_max.User'
3 MODELOS (CLAVE DEL PROYECTO)
Diseño de la Base De Datos Relacional en Diagrama Entidad-Relación  📁 car_max/models

Python
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('MANUAL', 'Manual'),
        ('AUTOMATIC', 'Automático'),
    ]
    
    FUEL_CHOICES = [
        ('GASOLINE', 'Gasolina'),
        ('DIESEL', 'Diésel'),
        ('ELECTRIC', 'Eléctrico'),
        ('HYBRID', 'Híbrido'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.CharField(max_length=50)
    model_name = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.PositiveIntegerField()
    transmission = models.CharField(max_length=15, choices=TRANSMISSION_CHOICES, default='AUTOMATIC')
    fuel_type = models.CharField(max_length=15, choices=FUEL_CHOICES, default='GASOLINE')
    engine = models.CharField(max_length=50)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cars'
    )
    
    categories = models.ManyToManyField(
        Category,
        related_name='cars'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model_name} ({self.year})"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    cars = models.ManyToManyField(
        Car,
        through='CartItem',
        related_name='carts'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido/Carrito {self.id} - {self.user}"


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'car'], name='unique_cart_car')
        ]

    def __str__(self):
        return f"{self.car} x {self.quantity}"
4 Admin de django
📁 car_max/admin:

Python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, Car, Cart, CartItem

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_seller', 'is_staff')
    list_filter = ('is_seller', 'is_staff', 'is_superuser')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información de Rol', {'fields': ('is_seller',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información de Rol', {'fields': ('is_seller',)}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model_name', 'year', 'price', 'transmission', 'fuel_type', 'owner')
    list_filter = ('brand', 'transmission', 'fuel_type', 'categories')
    search_fields = ('brand', 'model_name', 'description')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    inlines = [CartItemInline]
    readonly_fields = ('id', 'created_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'car', 'quantity')
5 Migraciones
Bash
python manage.py makemigrations
python manage.py migrate
6 Crear super useario
Bash
python manage.py createsuperuser
7 Ejecutar Servidor
Bash
python manage.py runserver
👉 Ir a:
http://127.0.0.1:8000/admin/

🚀 SPRINT 2 — Autenticación + UI Base
🎯 Objetivo
Registro, login, logout

Layout base con Bootstrap 5.3

Navbar dinámica (login / logout)

Listado de productos (cards)

Home pública

URLs del proyecto 📁 luxury_car/urls:
Python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Car_max.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
URLs de la app 📁 car_max/urls:
Python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cars/create/', views.car_create, name='car_create'),
    path('cars/<uuid:pk>/edit/', views.car_update, name='car_update'),
    path('cars/<uuid:pk>/delete/', views.car_delete, name='car_delete'),
]
Formularios 📁 car_max/forms:
Python
from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'brand', 'model_name', 'year', 'price', 'mileage', 
            'transmission', 'fuel_type', 'engine', 'description', 
            'stock', 'categories', 'image'
        ]
        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }
Vistas 📁 ca_max/views:
Python
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
Templates (Bootstrap 5.3) 📁 Crear la carpeta templates y dentro la carpeta store para agregar lo siguientes archivos de la Estructura que se muestra
Plaintext
templates/
 └── Car_max/
     ├── base.html
     ├── car_form.html
     ├── dashboard.html
     ├── home.html
     ├── login.html
     ├── product_confirm_delete.html
     ├── product_form.html
     └── register.html
🧩 base.html
HTML
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Car_max</title>

    <link href="[https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css](https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css)" rel="stylesheet">
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container">
    <a class="navbar-brand" href="/">Car_max</a>

    <div>
      {% if user.is_authenticated %}
        <span class="text-white me-3">Hola {{ user.username }}</span>
        <a href="{% url 'logout' %}" class="btn btn-outline-light btn-sm">Logout</a>
      {% else %}
        <a href="{% url 'login' %}" class="btn btn-outline-light btn-sm me-2">Login</a>
        <a href="{% url 'register' %}" class="btn btn-primary btn-sm">Registro</a>
      {% endif %}
    </div>
  </div>
</nav>

<div class="container mt-4">
    {% block content %}{% endblock %}
</div>

</body>
</html>
📋 car_form.html
HTML
{% extends 'Car_max/base.html' %}

{% block content %}

<h2>Ficha Técnica del Vehículo</h2>

<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}

    <button class="btn btn-primary">Guardar Vehículo</button>
</form>

{% endblock %}
📊 dashboard.html
HTML
{% extends 'Car_max/base.html' %}

{% block content %}

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Panel de Control - Inventario Exclusivo</h2>
    <a href="{% url 'car_create' %}" class="btn btn-success">+ Registrar Automóvil</a>
</div>

<table class="table table-striped align-middle">
    <thead>
        <tr>
            <th>Imagen</th>
            <th>Vehículo</th>
            <th>Año</th>
            <th>Precio</th>
            <th>Kilometraje</th>
            <th>Transmisión</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>

    {% for car in cars %}
        <tr>
            <td>
                {% if car.image %}
                    <img src="{{ car.image.url }}" alt="{{ car.model_name }}" style="width: 80px; height: auto; border-radius: 4px;">
                {% else %}
                    <span class="text-muted">Sin foto</span>
                {% endif %}
            </td>
            <td><strong>{{ car.brand }}</strong> {{ car.model_name }}</td>
            <td>{{ car.year }}</td>
            <td>${{ car.price }}</td>
            <td>{{ car.mileage }} km</td>
            <td>{{ car.get_transmission_display }}</td>
            <td>
                <a href="{% url 'car_update' car.id %}" class="btn btn-warning btn-sm">Editar</a>
                <a href="{% url 'car_delete' car.id %}" class="btn btn-danger btn-sm">Eliminar</a>
            </td>
        </tr>
    {% endfor %}

    </tbody>
</table>

{% endblock %}
🏠 home.html
HTML
{% extends 'Car_max/base.html' %}

{% block content %}

<h2 class="mb-4">Productos</h2>

<div class="row">
    {% for product in products %}
    <div class="col-md-4">
        <div class="card mb-4 shadow-sm">
            <div class="card-body">
                <h5>{{ product.name }}</h5>
                <p>{{ product.description|truncatechars:80 }}</p>

                <p><strong>$ {{ product.price }}</strong></p>

                <small class="text-muted">
                    Vendedor: {{ product.owner.username }}
                </small>

                <div class="mt-2">
                    {% for cat in product.categories.all %}
                        <span class="badge bg-secondary">{{ cat.name }}</span>
                    {% endfor %}
                </div>

            </div>
        </div>
    </div>
    {% empty %}
        <p>No hay productos aún.</p>
    {% endfor %}
</div>

{% endblock %}
🔐 login.html
HTML
{% extends 'Car_max/base.html' %}

{% block content %}

<h2>Login</h2>

<form method="POST">
    {% csrf_token %}
    <input type="text" name="username" placeholder="Usuario" class="form-control mb-2">
    <input type="password" name="password" placeholder="Contraseña" class="form-control mb-2">

    <button class="btn btn-primary">Ingresar</button>
</form>

{% endblock %}
⚠️ product_confirm_delete.html
HTML
{% extends 'Car_max/base.html' %}

{% block content %}

<h3>¿Retirar del catálogo el "{{ car.brand }} {{ car.model_name }}"?</h3>

<form method="POST">
    {% csrf_token %}
    <button class="btn btn-danger">Sí, eliminar</button>
    <a href="{% url 'dashboard' %}" class="btn btn-secondary">Cancelar</a>
</form>

{% endblock %}
📦 product_form.html
HTML
{% extends 'Car_max/base.html' %}

{% block content %}

<h2>Producto</h2>

<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}

    <button class="btn btn-primary">Guardar</button>
</form>

{% endblock %}
📝 register.html
HTML
{% extends 'Car_max/base.html' %}

{% block content %}

<h2>Registro</h2>

<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}

    <button class="btn btn-success">Registrarse</button>
</form>

{% endblock %}
Ejecutar el proyecto
Bash
python manage.py runserver
🧪 7. Flujo de prueba

Ir a /register/

Crear usuario

Login automático

Ver productos en /

Logout desde navbar

✅ Resultado del Sprint 2
✔ Autenticación completa
✔ UI base profesional con Bootstrap
✔ Navbar dinámica
✔ Listado de productos
✔ Estructura lista para escalar

