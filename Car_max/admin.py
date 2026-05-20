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