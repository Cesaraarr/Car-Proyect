# 🚀 SPRINT 1 — Setup + Configuración Base

## 🎯 Objetivo

Tener:

* Proyecto Django funcionando
* Aplicación `Car_max`
* Usuario personalizado
* Templates conectados
* Bootstrap 5.3 funcionando
* CRUD de vehículos
* Dashboard para vendedores

---

## 1 Crear proyecto Django

```bash
django-admin startproject Luxury_Car

cd Luxury_Car

python manage.py startapp Car_max
```

---

## 2 Configurar aplicación Django

📁 Car_max/apps.py

```python
from django.apps import AppConfig


class CarMaxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Car_max'
```

📌 Configura la aplicación principal:

```python
Car_max
```

---

## 3 Configurar settings.py

📁 Luxury_Car/settings.py

📌 Registrar aplicación

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Car_max'
]
```

📌 Usuario personalizado

```python
AUTH_USER_MODEL = 'Car_max.User'
```

📌 Base de datos SQLite

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

📌 Templates automáticos

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]
```

---

## 4 Configurar URLs globales

📁 Luxury_Car/urls.py

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Car_max.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
```

📌 Conecta todas las rutas de:

```python
Car_max.urls
```

---

📌 Activa el panel administrativo:

```bash
/admin/
```

---

📌 Permite mostrar imágenes usando:

```python
MEDIA_URL
```

---

# 🚀 SPRINT 2 — URLs + Vistas

## 🎯 Objetivo

Implementar:

* Home principal
* Registro
* Login
* Logout
* Dashboard
* CRUD de vehículos

---

## 1 Configurar URLs de la aplicación

📁 Car_max/urls.py

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('cars/create/', views.car_create, name='car_create'),

    path(
        'cars/<uuid:pk>/edit/',
        views.car_update,
        name='car_update'
    ),

    path(
        'cars/<uuid:pk>/delete/',
        views.car_delete,
        name='car_delete'
    ),
]
```

---

## 2 Vista Home

📁 Car_max/views.py

```python
def home(request):
    cars = Car.objects.all()[:6]
    return render(request, 'Car_max/home.html', {'cars': cars})
```

📌 Obtiene los primeros 6 vehículos registrados usando:

```python
Car.objects.all()[:6]
```

---

📌 Renderiza el template:

```python
Car_max/home.html
```

---

📌 Envía los datos usando:

```python
{'cars': cars}
```

---

## 3 Vista Register

📁 Car_max/views.py

```python
def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    else:

        form = UserCreationForm()

    return render(
        request,
        'Car_max/register.html',
        {'form': form}
    )
```

📌 Utiliza:

```python
UserCreationForm
```

para registrar usuarios.

---

📌 Después del registro ejecuta:

```python
login(request, user)
```

---

📌 Redirecciona hacia:

```python
home
```

---

## 4 Vista Login

📁 Car_max/views.py

```python
def login_view(request):

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            username = form.cleaned_data.get('username')

            password = form.cleaned_data.get('password')

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                return redirect('dashboard')

    else:

        form = AuthenticationForm()

    return render(
        request,
        'Car_max/login.html',
        {'form': form}
    )
```

📌 Utiliza:

```python
AuthenticationForm
```

para autenticar usuarios.

---

📌 Si el usuario existe:

```python
login(request, user)
```

---

📌 Después del login redirecciona a:

```python
dashboard
```

---

## 5 Vista Logout

📁 Car_max/views.py

```python
def logout_view(request):
    logout(request)
    return redirect('home')
```

📌 Cierra la sesión actual usando:

```python
logout(request)
```

---

📌 Después redirecciona hacia:

```python
home
```

---

# 🚀 SPRINT 3 — Dashboard + CRUD Vehículos

## 🎯 Objetivo

Implementar:

* Dashboard privado
* Crear vehículos
* Editar vehículos
* Eliminar vehículos
* Validación de propietario

---

## 1 Vista Dashboard

📁 Car_max/views.py

```python
@login_required
def dashboard(request):

    if not request.user.is_seller:
        return HttpResponseForbidden(
            "No tienes permisos"
        )

    cars = Car.objects.filter(
        owner=request.user
    )

    return render(
        request,
        'Car_max/dashboard.html',
        {'cars': cars}
    )
```

📌 Requiere autenticación usando:

```python
@login_required
```

---

📌 Verifica si el usuario es vendedor:

```python
request.user.is_seller
```

---

📌 Obtiene únicamente vehículos del usuario autenticado:

```python
Car.objects.filter(owner=request.user)
```

---

## 2 Crear Vehículo

📁 Car_max/views.py

```python
@login_required
def car_create(request):

    if not request.user.is_seller:
        return HttpResponseForbidden(
            "Solo vendedores autorizados"
        )

    form = CarForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():

        car = form.save(commit=False)

        car.owner = request.user

        car.save()

        form.save_m2m()

        return redirect('dashboard')

    return render(
        request,
        'Car_max/car_form.html',
        {'form': form}
    )
```

📌 Utiliza:

```python
CarForm
```

para registrar vehículos.

---

📌 Guarda imágenes usando:

```python
request.FILES
```

---

📌 Asigna automáticamente el propietario:

```python
car.owner = request.user
```

---

## 3 Editar Vehículo

📁 Car_max/views.py

```python
@login_required
def car_update(request, pk):

    car = get_object_or_404(
        Car,
        pk=pk
    )

    if car.owner != request.user:
        return HttpResponseForbidden(
            "No puedes editar este vehículo"
        )

    form = CarForm(
        request.POST or None,
        request.FILES or None,
        instance=car
    )

    if form.is_valid():

        form.save()

        return redirect('dashboard')

    return render(
        request,
        'Car_max/car_form.html',
        {'form': form}
    )
```

📌 Obtiene el vehículo usando:

```python
get_object_or_404()
```

---

📌 Verifica que el propietario sea el usuario autenticado.

---

📌 Reutiliza:

```python
car_form.html
```

---

## 4 Eliminar Vehículo

📁 Car_max/views.py

```python
@login_required
def car_delete(request, pk):

    car = get_object_or_404(
        Car,
        pk=pk
    )

    if car.owner != request.user:
        return HttpResponseForbidden(
            "No puedes eliminar este vehículo"
        )

    if request.method == 'POST':

        car.delete()

        return redirect('dashboard')

    return render(
        request,
        'Car_max/car_confirm_delete.html',
        {'car': car}
    )
```

📌 Elimina vehículos usando:

```python
car.delete()
```

---

📌 Utiliza confirmación previa con:

```python
car_confirm_delete.html
```

---

# 🚀 SPRINT 4 — Formularios

## 🎯 Objetivo

Implementar formularios usando Django Forms.

---

## 1 Formulario de Vehículos

📁 Car_max/forms.py

```python
from django import forms
from .models import Car


class CarForm(forms.ModelForm):

    class Meta:

        model = Car

        fields = [
            'brand',
            'model_name',
            'year',
            'price',
            'mileage',
            'transmission',
            'fuel_type',
            'engine',
            'description',
            'stock',
            'categories',
            'image'
        ]

        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }
```

📌 El formulario utiliza el modelo:

```python
Car
```

---

📌 Permite subir imágenes usando:

```python
image
```

---

📌 Las categorías se renderizan usando:

```python
CheckboxSelectMultiple
```

---

# 🚀 SPRINT 5 — Templates HTML

## 🎯 Objetivo

Implementar interfaz visual usando Bootstrap 5.3.

---

## 1 Template Base

📁 templates/Car_max/base.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">

    <title>Car_max</title>

    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
        rel="stylesheet">
</head>
```

📌 Importa Bootstrap 5.3 usando CDN.

---

## 2 Navbar principal

📁 templates/Car_max/base.html

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
```

📌 Utiliza Bootstrap Navbar.

---

📌 Muestra el nombre:

```html
Car_max
```

---

📌 Verifica autenticación usando:

```html
{% if user.is_authenticated %}
```

---

## 3 Dashboard HTML

📁 templates/Car_max/dashboard.html

```html
{% for car in cars %}
```

📌 Recorre todos los vehículos enviados desde:

```python
views.dashboard
```

---

📌 Muestra:

* imagen
* marca
* modelo
* año
* precio
* kilometraje
* transmisión

---

📌 Permite:

* editar
* eliminar

---

## 4 Formulario Vehículos

📁 templates/Car_max/car_form.html

```html
<form method="POST" enctype="multipart/form-data">
```

📌 Permite enviar imágenes usando:

```html
multipart/form-data
```

---

📌 Utiliza:

```html
{{ form.as_p }}
```

para renderizar automáticamente el formulario.

---

# 🚀 SPRINT 6 — Panel Administrativo

## 🎯 Objetivo

Registrar modelos en Django Admin.

---

## 1 Configurar admin.py

📁 Car_max/admin.py

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    User,
    Category,
    Car,
    Cart,
    CartItem
)
```

---

## 2 Registrar Usuario

📁 Car_max/admin.py

```python
@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_display = (
        'username',
        'email',
        'is_seller',
        'is_staff'
    )
```

📌 Extiende:

```python
BaseUserAdmin
```

---

📌 Muestra:

* username
* email
* is_seller
* is_staff

---

## 3 Registrar Vehículos

📁 Car_max/admin.py

```python
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    list_display = (
        'brand',
        'model_name',
        'year',
        'price',
        'transmission',
        'fuel_type',
        'owner'
    )
```

📌 Muestra información principal de vehículos.

---

📌 Implementa filtros usando:

```python
list_filter
```

---

📌 Implementa búsqueda usando:

```python
search_fields
```

---

# 🧪 Flujo de prueba

1 Crear superusuario

```bash
python manage.py createsuperuser
```

2 Ejecutar servidor

```bash
python manage.py runserver
```

3 Entrar a:

```bash
http://127.0.0.1:8000/
```

4 Registrar usuario

5 Iniciar sesión

6 Entrar al dashboard

7 Registrar vehículo

8 Editar vehículo

9 Eliminar vehículo

10 Entrar al panel admin

---

# ✅ Resultado Final

```bash
✔ Proyecto Django funcionando
✔ Usuario personalizado
✔ CRUD de vehículos
✔ Dashboard privado
✔ Login y registro
✔ Templates Bootstrap
✔ Panel administrativo
✔ Gestión de imágenes
✔ Formularios Django
```