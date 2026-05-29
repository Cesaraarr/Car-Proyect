# 🚀 SPRINT 1 — Setup Inicial + Configuración Base

## 🎯 Objetivo

En esta primera etapa construiremos la base del sistema **Car_max**.

Al finalizar este Sprint tendremos:

- ✔ Proyecto Django funcionando
- ✔ Aplicación `Car_max`
- ✔ Usuario personalizado
- ✔ Configuración de rutas
- ✔ Templates conectados
- ✔ Bootstrap 5.3 funcionando
- ✔ Arquitectura inicial lista para escalar

---

# 🧱 1️⃣ Crear Proyecto Django

## 📌 ¿Qué haremos?

Crearemos:

- Proyecto principal → `luxury_car`
- Aplicación → `Car_max`

---

## ⚙️ Comandos de instalación

```bash
django-admin startproject luxury_car

cd luxury_car

python manage.py startapp Car_max
```

---

## 📌 Explicación

### `startproject luxury_car`

Crea el proyecto principal Django.

Aquí vive:

- configuración global
- settings
- urls
- wsgi
- asgi

---

### `startapp Car_max`

Crea la aplicación donde estará toda la lógica del marketplace.

Aquí estarán:

- modelos
- vistas
- formularios
- templates
- lógica del negocio

---

# 🧱 2️⃣ Registrar la Aplicación

## 📁 luxury_car/settings.py

## 📌 Agregar `Car_max` en INSTALLED_APPS

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

---

## 📌 Explicación

Django necesita saber qué aplicaciones existen dentro del proyecto.

Cuando agregamos:

```python
'Car_max'
```

Django automáticamente:

- detecta modelos
- habilita templates
- registra migraciones
- conecta admin.py
- carga urls internas

---

# 🧱 3️⃣ Usuario Personalizado

## 📁 luxury_car/settings.py

```python
AUTH_USER_MODEL = 'Car_max.User'
```

---

## 📌 ¿Por qué usamos un User personalizado?

Porque más adelante necesitaremos:

- vendedores
- compradores
- roles
- permisos
- dashboards

El modelo por defecto de Django es limitado.

Por eso creamos:

```python
class User(AbstractUser)
```

---

# 🧱 4️⃣ Configuración de URLs Globales

## 📁 luxury_car/urls.py

```python
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # =========================
    # ⚙️ Admin Django
    # =========================
    path('admin/', admin.site.urls),

    # =========================
    # 🚘 App Car_max
    # =========================
    path('', include('Car_max.urls')),
]

# =========================
# 🖼️ Archivos multimedia
# =========================
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
```

---

## 📌 Explicación

### `include('Car_max.urls')`

Le dice a Django:

> “Todas las rutas principales estarán dentro de la aplicación Car_max”.

---

### `static(...)`

Permite mostrar:

- imágenes
- fotografías de vehículos
- archivos multimedia

durante desarrollo.

---

# 🧱 5️⃣ Crear URLs de la Aplicación

## 📁 Car_max/urls.py

```python
from django.urls import path

from . import views

urlpatterns = [

    # =========================
    # 🏠 Home
    # =========================
    path('', views.home, name='home'),

    # =========================
    # 🔐 Autenticación
    # =========================
    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # =========================
    # 📊 Dashboard
    # =========================
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # =========================
    # 🚘 CRUD Vehículos
    # =========================
    path(
        'cars/create/',
        views.car_create,
        name='car_create'
    ),

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

# 📌 Explicación General de URLs

## 🏠 Home

```python
path('', views.home, name='home')
```

Página principal del sistema.

Aquí mostraremos:

- catálogo
- vehículos destacados
- cards Bootstrap

---

## 🔐 Login y Registro

Permiten:

- autenticación
- sesiones
- acceso al dashboard

---

## 📊 Dashboard

Panel privado para vendedores.

Aquí podrán:

- crear autos
- editar autos
- eliminar autos

---

## 🚘 CRUD Vehículos

CRUD significa:

- Create
- Read
- Update
- Delete

Es decir:

- registrar vehículo
- editar vehículo
- eliminar vehículo

---

# 🧱 6️⃣ Crear Estructura de Templates

## 📌 Crear carpetas

```bash
templates/
└── Car_max/
```

---

## 📌 Dentro crear:

```bash
base.html

home.html

login.html

register.html

dashboard.html

car_form.html

product_confirm_delete.html
```

---

# 🧱 7️⃣ Template Base

## 📁 templates/Car_max/base.html

```html
<!DOCTYPE html>
<html lang="es">
<head>

    <meta charset="UTF-8">

    <title>Car_max</title>

    <!-- Bootstrap 5.3 -->
    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
        rel="stylesheet">

</head>

<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark">

  <div class="container">

    <a class="navbar-brand" href="/">
        Car_max
    </a>

    <div>

      {% if user.is_authenticated %}

        <span class="text-white me-3">
            Hola {{ user.username }}
        </span>

        <a href="{% url 'logout' %}"
           class="btn btn-outline-light btn-sm">
           Logout
        </a>

      {% else %}

        <a href="{% url 'login' %}"
           class="btn btn-outline-light btn-sm me-2">
           Login
        </a>

        <a href="{% url 'register' %}"
           class="btn btn-primary btn-sm">
           Registro
        </a>

      {% endif %}

    </div>

  </div>

</nav>

<div class="container mt-4">

    {% block content %}
    {% endblock %}

</div>

</body>
</html>
```

---

# 📌 Explicación del Template Base

## 🧩 ¿Qué es `base.html`?

Es la plantilla principal del proyecto.

Todos los demás templates heredarán de aquí usando:

```html
{% extends 'Car_max/base.html' %}
```

---

## 🎨 Bootstrap 5.3

```html
<link
href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
```

Nos permite usar:

- navbar
- botones
- cards
- tablas
- formularios modernos
- sistema responsive

---

## 🔐 Navbar dinámica

```html
{% if user.is_authenticated %}
```

Verifica si el usuario inició sesión.

Si inició sesión:

- muestra saludo
- muestra logout

Si NO inició sesión:

- login
- registro

---