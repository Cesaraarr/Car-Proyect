# 🚀 SPRINT 1 — Setup Inicial + Arquitectura Base

## 🎯 Objetivo

En esta primera etapa construiremos toda la estructura inicial del proyecto **Car_max**, un marketplace de vehículos de lujo desarrollado con Django.

Al finalizar este Sprint tendremos:

- ✔ Proyecto Django funcionando
- ✔ Aplicación `Car_max`
- ✔ Configuración inicial del sistema
- ✔ Usuario personalizado
- ✔ Arquitectura MVT
- ✔ Templates conectados
- ✔ Bootstrap 5.3 integrado
- ✔ Sistema listo para escalar

---

# 🧱 1️⃣ Crear Proyecto Django

## 📌 ¿Qué haremos?

Crearemos:

- Proyecto principal → `Luxury_Car`
- Aplicación → `Car_max`

---

## ⚙️ Comandos de instalación

```bash
django-admin startproject Luxury_Car

cd Luxury_Car

python manage.py startapp Car_max
```

---

# 📌 Explicación

## `startproject Luxury_Car`

Crea el núcleo principal del proyecto Django.

Aquí viven:

- settings globales
- urls globales
- configuración WSGI
- configuración ASGI
- seguridad
- middlewares

---

## `startapp Car_max`

Crea el módulo donde estará toda la lógica del marketplace automotriz.

Aquí estarán:

- modelos
- vistas
- formularios
- templates
- autenticación
- CRUD
- dashboard
- carrito

---

# 🧱 2️⃣ Arquitectura del Proyecto

## 📁 Estructura principal

```bash
CAR-PROYECT/
│
├── Car_max/
│   ├── migrations/
│   ├── templates/
│   │   └── Car_max/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── dashboard.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── car_form.html
│   │       ├── product_form.html
│   │       └── product_confirm_delete.html
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── Luxury_Car/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── db.sqlite3
└── manage.py
```

---

# 📌 Explicación de la Arquitectura

## 📁 Car_max/

Contiene toda la lógica del marketplace.

Aquí se desarrolla:

- backend
- frontend
- ORM
- autenticación
- templates
- CRUD

---

## 📁 templates/

Contiene todas las vistas HTML del sistema.

---

## 📁 Luxury_Car/

Contiene la configuración global del proyecto Django.

---

## 📁 db.sqlite3

Base de datos SQLite utilizada durante desarrollo.

---

# 🧱 3️⃣ Configuración de la Aplicación

## 📁 Car_max/apps.py

```python
from django.apps import AppConfig


class CarMaxConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'

    name = 'Car_max'
```

---

# 📌 Explicación

## `AppConfig`

Representa la configuración interna de la aplicación Django.

---

## `default_auto_field`

Define el tipo de llave primaria automática por defecto.

En este caso:

```python
BigAutoField
```

usa enteros grandes para IDs automáticos.

---

## `name = 'Car_max'`

Le indica a Django el nombre oficial de la aplicación.

Esto permite:

- registrar modelos
- cargar templates
- detectar migraciones
- conectar URLs

---

# 🧱 4️⃣ Configuración Global del Proyecto

## 📁 Luxury_Car/settings.py

---

# 🔐 Configuración principal

```python
SECRET_KEY = 'django-insecure...'
```

---

# 📌 Explicación

La `SECRET_KEY` es utilizada por Django para:

- cifrado de sesiones
- tokens CSRF
- seguridad
- autenticación

⚠️ Nunca debe compartirse en producción.

---

# 🧱 Modo desarrollo

```python
DEBUG = True
```

---

# 📌 Explicación

Permite:

- ver errores detallados
- depuración
- recarga automática

⚠️ En producción debe ser:

```python
DEBUG = False
```

---

# 🧱 Hosts permitidos

```python
ALLOWED_HOSTS = []
```

---

# 📌 Explicación

Define qué dominios pueden acceder al proyecto.

En desarrollo normalmente queda vacío.

---

# 🧱 Usuario Personalizado

```python
AUTH_USER_MODEL = 'Car_max.User'
```

---

# 📌 Explicación

Django normalmente usa:

```python
auth.User
```

Pero nosotros creamos un usuario personalizado porque necesitamos:

- vendedores
- compradores
- permisos
- dashboards
- roles especiales

---

# 🧱 Aplicaciones instaladas

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

# 📌 Explicación

## Apps internas de Django

### `django.contrib.admin`

Activa el panel administrativo.

---

### `django.contrib.auth`

Sistema de autenticación.

---

### `django.contrib.sessions`

Permite sesiones de usuario.

---

### `django.contrib.messages`

Permite mensajes dinámicos.

---

### `django.contrib.staticfiles`

Manejo de archivos estáticos:

- CSS
- JS
- imágenes

---

## App personalizada

```python
'Car_max'
```

Registra nuestra aplicación automotriz.

---

# 🧱 Middlewares

```python
MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

---

# 📌 Explicación

Los middlewares procesan cada petición HTTP.

Ejemplos:

| Middleware | Función |
|---|---|
| SecurityMiddleware | Seguridad |
| SessionMiddleware | Manejo de sesiones |
| AuthenticationMiddleware | Login de usuarios |
| CsrfViewMiddleware | Protección CSRF |

---

# 🧱 Templates

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

# 📌 Explicación

## `APP_DIRS = True`

Le dice a Django:

> “Busca automáticamente carpetas templates dentro de cada app”.

Por eso funciona:

```bash
templates/Car_max/
```

---

# 🧱 Base de Datos

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

# 📌 Explicación

El proyecto utiliza:

```bash
SQLite3
```

Ventajas:

- ligera
- rápida
- no requiere instalación
- perfecta para desarrollo

---

# 🧱 Internacionalización

```python
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
```

---

# 📌 Explicación

Define:

- idioma del sistema
- zona horaria
- traducciones
- manejo de fechas

---

# 🧱 Archivos estáticos

```python
STATIC_URL = 'static/'
```

---

# 📌 Explicación

Permite servir:

- CSS
- JavaScript
- imágenes estáticas

---

# 🧱 Tipo de ID por defecto

```python
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

---

# 📌 Explicación

Define IDs automáticos grandes para nuevos modelos.

---

# 🧱 5️⃣ Configuración de URLs Globales

## 📁 Luxury_Car/urls.py

```python
from django.contrib import admin

from django.urls import path, include

from django.conf import settings

from django.conf.urls.static import static


urlpatterns = [

    # =========================
    # ⚙️ Panel Admin
    # =========================
    path('admin/', admin.site.urls),

    # =========================
    # 🚘 Aplicación Car_max
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

# 📌 Explicación

## `admin.site.urls`

Activa:

```bash
/admin/
```

Panel administrativo Django.

---

## `include('Car_max.urls')`

Conecta las rutas internas de la aplicación.

---

## `static(...)`

Permite mostrar imágenes durante desarrollo.

Muy importante porque el modelo `Car` usa:

```python
ImageField
```

---