from django.contrib import admin
from account.models import *

@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    pass