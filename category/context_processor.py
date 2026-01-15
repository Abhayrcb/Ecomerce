from category.models import Category
from cart.models import Cart
from cart.views import _cart_id


def categories(request):
    
    links = Category.objects.all()
    return {'links': links}


def Cart_notification(request):
    count =0
    try:
       cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = None
    cart_items = cart.cartitem_set.all()
    for item in cart_items:
        count += item.quantity
    return { 'count': count}

