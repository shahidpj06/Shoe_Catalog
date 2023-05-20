from .views import ProductList, checkout, add_to_cart
from django.urls import path

urlpatterns = [
    path('product/', ProductList.as_view(), name = 'products'),
    path('checkout/', checkout, name='checkout'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

]