from django.urls import path
from cart.views import *

app_name = "cart"

urlpatterns = [
    path('', cart_summary, name='cart_summary'),
    path('add/', cart_add, name='card_add'),
    path('delete/', cart_delete, name='cart_delete'),
    path('update/', cart_update, name='cart_update'),
]