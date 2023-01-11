from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, ValidationError
from store.models import Product
from datetime import datetime

def only_int(value):
    try:
        value = int(value)
        return value
    except:
        raise ValidationError('Zip code must contain only numbers')

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=150)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=6, validators=[
        MinLengthValidator(4),
        only_int,
    ])

    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return self.user.username

    def get_full_address(self):
        return self.address1 + "," + self.address2 + "," + self.city + "," + self.state + "," + self.zipcode

class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    shipping_address = models.TextField(max_length=10000)
    amount_total = models.DecimalField(max_digits=8, decimal_places=2)
    date_ordered = models.DateTimeField(default=datetime.now(), editable=False)

    def __str__(self):
        return "Order " + str(self.id)

class OrderItem(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "Order Item " + str(self.id)