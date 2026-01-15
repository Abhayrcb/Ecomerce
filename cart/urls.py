from django.urls import path
from .views import cart,add_cart,decrease_cart,delete_cart,increase_cart,checkout

urlpatterns = [
    path('',cart,name='cart'),
    path('add_cart/<int:product_id>/',add_cart, name='add_cart'),
    path('decrease_cart/<int:product_id>/',decrease_cart, name='decrease_cart'),
    path('delete_cart/<int:product_id>/',delete_cart, name='delete_cart'),
    path('increase_cart/<int:product_id>/',increase_cart, name='increase_cart'),
    path('checkout/', checkout, name='checkout'),
]
