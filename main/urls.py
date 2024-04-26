from django.urls import path
from main.views import *

urlpatterns = [
    path('', index, name='home'),
    path('catalog/', catalog, name='catalog'),
    path('product/<int:product_id>/', product, name='product'),
    path('about/', about, name='about'),
    path('wherefind/', wherefind, name='wherefind')
]