from django.shortcuts import render,redirect
from store.models import Product,Variation
from .models import Cart,CartItem
from django.contrib.auth.decorators import login_required
from orders.forms import OrderForm
from django.views.generic import ListView
# Create your views here.
def cart(request,total_price=0,quantity=0,cart_item=None):
   
    cart_item = CartItem.objects.all().filter(user=request.user) if request.user.is_authenticated else CartItem.objects.all().filter(cart__cart_id=_cart_id(request))
    
    for item in cart_item:
        # har ek item ke product price*quantity ko total price me add karte jao
        total_price += (item.product.price * item.quantity)
        quantity += item.quantity
    
     # sabhi product item pe ek sath add karke 2% tax
    tax = (2 * total_price)/100
    grand_total = total_price + tax
    return render(request, 'cart.html', {'cart_item': cart_item, 'total_price': total_price, 'quantity': quantity,'tax':tax,'grand_total':grand_total})



    


# private function for retrieving the cart id or creating a new one
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



def add_cart(request,product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    product_variation = []
    if  request.POST.get('color') or request.POST.get('size'):
        
         for key in request.POST:
            category = key
            value = request.POST[key]
            if key != 'csrfmiddlewaretoken':
                try:
                    variation = Variation.objects.get(product=product,variation_category__iexact=category,variation_value__iexact=value)
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    pass

    
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()
        
    try:
        if user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=user)
        else:
            cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        for item in product_variation:
            cart_item.variation.add(item)
        cart_item.save()
        
        
    except CartItem.DoesNotExist:
        if user.is_authenticated:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = user
            )
        else:   
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart
            )
        for item in product_variation:
            cart_item.variation.add(item)
        cart_item.save()
        
    return redirect('cart')

def decrease_cart(request,product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(product=product,user=request.user)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(product=product,cart=cart)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def delete_cart(request,product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(product=product,user=request.user)
        cart_item.delete()
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.delete()
    return redirect('cart')

def increase_cart(request,product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(product=product,user=request.user)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(product=product,cart=cart)
        
        
    if product.stock > cart_item.quantity:
        cart_item.quantity += 1
        cart_item.save()    
    return redirect('cart')




@login_required
def checkout(request):
    cart_item = CartItem.objects.all().filter(user=request.user)
    return render(request, 'store/checkout.html', {'cart_items': cart_item})



