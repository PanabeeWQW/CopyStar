from django.shortcuts import render
from .models import *

def index(request):
    return render(request, 'main/index.html')

def catalog(request):
    product = Product.objects.all
    return render(request, 'main/catalog/catalog.html', {'product': product})

def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'main/product/product.html', {'product': product})
def about(request):
    return render(request, 'main/about.html')

def wherefind(request):
    return render(request, 'main/wherefind.html')