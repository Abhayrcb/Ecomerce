from django.urls import path
from .views import place_order,payment
urlpatterns = [
    path('place_order/',place_order,name='place_order'),
    path('payments/',payment,name='payment'),
]
