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


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )

    categories = models.ManyToManyField(
        Category,
        related_name='products'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts'
    )

    products = models.ManyToManyField(
        Product,
        through='CartItem',
        related_name='carts'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} - {self.user}"


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product'], name='unique_cart_product')
        ]

    def __str__(self):
        return f"{self.product} x {self.quantity}"