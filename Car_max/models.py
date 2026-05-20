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