from django.shortcuts import render, get_object_or_404
from store.models import *

def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}

def products(request):
    all_products = Product.objects.all()
    return {'all_products': all_products}

def store(request):
    return render(request, 'store/store.html', context={'title': 'Product Destination | Store', 'category': None})

def product_info(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_info.html', context={'title': product.title.replace('-', ' ').title(), 'product': product})

def search(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, 'store/store.html', context={'title': 'Product Destination | Store', 'category': category})