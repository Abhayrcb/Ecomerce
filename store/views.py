from django.shortcuts import render,get_object_or_404
from category.models import Category
from store.models import Product
from cart.models import Cart,CartItem
from cart.views import _cart_id
from django.core.paginator import Paginator
from django.http import HttpResponse    
# Create your views here.
def store(request,category_slug=None):
    
    
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories,is_available=True)
        paginator = Paginator(products, 6)
        current_page = request.GET.get('page')
        current_page_products = paginator.get_page(current_page)
        product_count = products.count()
        
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        current_page = request.GET.get('page')
        current_page_products = paginator.get_page(current_page)
        product_count = products.count()
    
    return render(request, 'store/store.html',{'products': current_page_products, 'product_count': product_count})



def single_page(request,category_slug,product_slug):
    
    try:
        product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product).exists()
        
        
    except Exception as e:
        raise e
    return render(request, 'store/singlepage.html', {'product': product, 'in_cart': in_cart})


def search_page(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(description__icontains=keyword)
            product_count = products.count()
    return render(request, 'store/search.html', {'products': products, 'product_count': product_count})