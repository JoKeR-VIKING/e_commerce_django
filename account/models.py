from django.db import models
from django.contrib.auth.models import User

class UserCart(models.Model):
    username = models.CharField(max_length=150, unique=True)
    user_cart = models.JSONField(default=dict, null=True, blank=True)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)

    def __str__(self):
        return self.username

User._meta.get_field('email')._unique = True