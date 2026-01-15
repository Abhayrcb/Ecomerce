from django.db import models
from store.models import Product,Variation
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"

    
class CartItem(models.Model):
    user    = models.ForeignKey('accounts.Account',on_delete=models.CASCADE,null=True,blank=True)
    product  = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation,blank=True)
    cart     = models.ForeignKey(Cart,null=True,blank=True,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active= models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.product)
    
    def sub_total(self):
        return self.product.price * self.quantity