from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=300, default='windsor')

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def refill(self, name1):
        product = Product.objects.get(name=name1)
        product.stock = product.stock + 100
        product.save()
        return self.stock

class Client(User):
    PROVINCE_CHOICES = [
        ('AB', 'Alberta'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    ]
    company = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=30, default='windsor')

    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20)
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)
    picture = models.ImageField(upload_to='myapp/images', null=True, blank=True)

    def __str__(self):
        return self.username

class Order(models.Model):
    STATUS_CHOICES = [
                    (0, 'Order Cancelled'),
                    (1, 'Order Placed'),
                    (2, 'Order Shipped'),
                    (3, 'Order Delivered'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_unit = models.PositiveIntegerField(default=100)
    order_status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    status_date = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.product)


    def total_cost(self, product):
        od = Order.objects.filter(product__name=product)
        pr = Product.objects.filter(name=product)
        x = pr.values()[0].get('price')
        y = od.values()[0].get('num_unit')
        return x*y

class ImagesTable(models.Model):
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='myapp/images')
    client = models.OneToOneField(Client, on_delete=models.CASCADE)

