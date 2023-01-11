from django.urls import path
from payment.views import *

app_name = 'payment'

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('complete_order/', complete_order, name='complete_order'),
    path('my_orders/', my_orders, name='my_orders'),
]
