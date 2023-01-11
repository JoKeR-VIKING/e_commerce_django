from django.urls import path
from store.views import *

app_name = "store"

urlpatterns = [
    path('', store, name='store'),
    path('product_info/<slug:slug>/', product_info, name='product_info'),
    path('search/<slug:slug>/', search, name='search'),
]
