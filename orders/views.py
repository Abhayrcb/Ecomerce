from django.shortcuts import render,redirect
from cart.models import CartItem
from orders.forms import OrderForm
from orders.models import Order

# Create your views here.
import datetime
import razorpay



  
 




def place_order(request):
    total_price =0
    tax=0
    user = request.user
    cart_item = CartItem.objects.filter(user=user)
    print(cart_item.count())
    if cart_item.count() <=0:
        return redirect('store')
    
    
    for item in cart_item:
        # har ek item ke product price*quantity ko total price me add karte jao
        total_price += (item.product.price * item.quantity)
       
    
     # sabhi product item pe ek sath add karke 2% tax
    tax = (2 * total_price)/100
    grand_total = total_price + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            
            data = Order()
            data.user = user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.ip = request.META.get('REMOTE_ADDR')
            data.tax = tax
            data.order_total = grand_total
            data.save()
            
            yt = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            
            d = (datetime.date(yt,mt,dt)).strftime('%y%m%d')
            
            data.order_number = d + str(data.id)
            
            data.save()
            
            try:
               razorpay_amount = int(grand_total * 100)
               client = razorpay.Client(auth=("rzp_test_S2DneIXVIdUUTF","D4lF4GaRhMSFYU7M3hLZqpPM"))
               razorpay_order = client.order.create({
                "amount": razorpay_amount,  # paisa
                "currency": "INR",
                "payment_capture": 1
            })
               print(client)
               print(razorpay_order)
            except Exception as e:
                print(e)
            
            
            
            return render(request,'order/PaymentPage.html',{'order':data,'grand_total':grand_total,'tax':tax,'cart_item':cart_item,'razorpay_order_id': razorpay_order['id'],'razorpay_amount':razorpay_amount,
                'razorpay_key': 'rzp_test_S2DneIXVIdUUTF',})

    return redirect('checkout')
    
    
    
def payment(request):
    # return render(request,'order/PaymentPage.html')
    pass