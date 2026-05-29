# 🚀 Primeros pasos - (Luxury Car)

## 🎯 Objetivo

Tener la estructura inicial para la plataforma de venta de autos de lujo:

* Proyecto Django funcionando (`Luxury_Car`)
* App store operativa (`Car_max`)
* Modelos con relaciones:
    * 1:N → Usuario (Vendedor/Admin) → Producto (Auto de Lujo)
    * N:M → Producto (Auto) ↔ Categoría (Deportivos, SUV, Eléctricos)
    * N:M → Carrito ↔ Producto (a través de la tabla intermedia `CartItem`)
* Admin operativo para gestionar el inventario

---

## 1 Crear proyecto en django

Para replicar el entorno de desarrollo y la estructura base del proyecto, se ejecutan los siguientes comandos en la terminal:

```bash
# Crear el proyecto principal de Django
django-admin startproject Luxury_Car

# Entrar a la carpeta raíz del proyecto
cd Luxury_Car

# Crear la aplicación para la gestión de los autos
python manage.py startapp Car_max