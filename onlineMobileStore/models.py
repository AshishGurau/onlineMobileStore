from contextlib import nullcontext
from unicodedata import category, name
from django.contrib.auth.models import User
from django.db import models
from matplotlib.pyplot import cla
from pyrsistent import b


# Create your models here.
class Category(models.Model):
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(null=True, blank=True)
    small_description = models.CharField(max_length=250, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    tag = models.CharField(max_length=150, null=False, blank=False)
   
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def get_photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

class Sale(models.Model):
    image = models.ImageField(null=True, blank=True)
    p_name = models.CharField(max_length=30)
    price = models.IntegerField()

    def __str__(self):
        return self.p_name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordared = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
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
    product = models.ForeignKey(Sale, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True,  null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address   



class SpecialPrice(models.Model):
    
    p_name = models.CharField(max_length=30)
    price = models.IntegerField()

    def __str__(self):
        return self.p_name

class NewPhone(models.Model):
    image = models.ImageField(null=True, blank=True)
    p_name = models.CharField(max_length=30)
    price = models.IntegerField()

    def __str__(self):
        return self.p_name

class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    general = models.CharField(max_length=200, null=False, blank=False)
    displayType = models.CharField(max_length=200, null=False, blank=False)
    memory = models.CharField(max_length=200, null=False, blank=False)
    wlan = models.CharField(max_length=200, null=False, blank=False)
    usb = models.CharField(max_length=200, null=False, blank=False)
    cameraPrimary = models.CharField(max_length=200, null=False, blank=False)
    cameraVideo = models.CharField(max_length=200, null=False, blank=False)
    cameraSecondary = models.CharField(max_length=200, null=False, blank=False)
    os = models.CharField(max_length=200, null=False, blank=False)
    chipset = models.CharField(max_length=200, null=False, blank=False)
    cpu = models.CharField(max_length=200, null=False, blank=False)
    battery = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.product.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def getCart_items(self):
        items = self.cart_set.all()
        total = sum([item.product_qty for item in items])
        return total