from django.shortcuts import render
from store.models import Product

def home(req):
    try:
        
       products = Product.objects.all().filter(is_available=True)
    except Product.DoesNotExist:
        products = None
    return render(req,'home.html',{'products':products})