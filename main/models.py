from django.db import models
from django.contrib.auth.models import User

class PhoneVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='phone_verification')
    phone_number = models.CharField(max_length=15, unique=True)
    verification_code = models.CharField(max_length=6, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number
    

class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200)
    desc = models.TextField(null=True)
    price = models.IntegerField(default=0, null=True, blank=True)
    weight = models.IntegerField(default=0, null=True, blank=True)
    new = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    order_id = models.AutoField(primary_key=True)
    complete = models.BooleanField(default=False)
    sended = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order_id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems]) 
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems]) 
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.TextField(null=True)
    orderType = models.CharField(max_length=10)
    paymentType = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.address