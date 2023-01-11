from django.contrib import admin
from store.models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ['id']
    prepopulated_fields = {'slug': ['name']}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ['id']
    prepopulated_fields = {'slug': ['brand', 'title']}
