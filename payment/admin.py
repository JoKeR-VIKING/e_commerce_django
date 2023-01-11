from django.contrib import admin
from payment.models import *

@admin.register(ShippingAddress)
class ShippingAdmin(admin.ModelAdmin):
    ordering = ['user']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ['id']
    readonly_fields = ['id', 'date_ordered']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    ordering = ['id']
    readonly_fields = ['id']