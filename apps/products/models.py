import datetime
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/images', null=True, blank=True)

    STATUS = [
        (True, 'Mavjud'),
        (False, 'Mavjud emas'),
    ]

    status = models.BooleanField(choices=STATUS, default=True)

    @property
    def image_url(self):
        if self.image:
            if settings.DEBUG:
                return f'{settings.LOCAL_BASE_URL}{self.image.url}'
            return f'{settings.PROD_BASE_URL}{self.image.url}'
        else:
            return None

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category_product'
    )

    name = models.CharField(max_length=120)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    STATUS = [

        (True, 'Mavjud'),
        (False, 'Mavjud emas')

    ]

    status = models.BooleanField(choices=STATUS, default=STATUS[1][1])

    # @property
    # def category(self):
    #     return self.category_set.all()

    def __str__(self):
        return f"{self.name}"


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_images')
    image = models.ImageField(upload_to='product/images', null=True, blank=True)

    @property
    def image_url(self):
        if self.image:
            if settings.DEBUG:
                return f'{settings.LOCAL_BASE_URL}{self.image.url}'
            return f'{settings.PROD_BASE_URL}{self.image.url}'
        else:
            return None

    def __str__(self):
        return self.product.name


class Room(models.Model):
    name = models.CharField(max_length=120)
    room_number = models.IntegerField(default=101)
    room_capacity = models.IntegerField(default=4)
    price = models.FloatField(default=100.000)

    BOOKING = [
        (True, 'enable'),
        (False, 'disable'),
    ]

    booking = models.BooleanField(choices=BOOKING, default=True)

    IS_BOOKED = [
        (True, 'Booked'),
        (False, 'Not booked'),
    ]

    is_booked = models.BooleanField(max_length=90, choices=IS_BOOKED, default=False)

    def __str__(self):
        return self.name


class RoomImages(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='room_images')
    image = models.ImageField(upload_to='room/images', null=True, blank=True)

    @property
    def image_url(self):
        if self.image:
            if settings.DEBUG:
                return f'{settings.LOCAL_BASE_URL}{self.image.url}'
            return f'{settings.PROD_BASE_URL}{self.image.url}'
        else:
            return None


class Booking(models.Model):
    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='room_booking')
    reservation_date = models.DateTimeField(default=datetime.datetime.now())
    number_of_guest = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['reservation_date', 'guest']
        ordering = ['-created']

    def __str__(self):
        return self.guest


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order_address = models.CharField(max_length=100)

    STATUS = [
        ('new', 'New'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
        ('process', 'Process'),
    ]

    status = models.CharField(max_length=90, choices=STATUS, default=STATUS[0][0])

    @property
    def order_total_price(self):
        items = self.order_items.all()
        total = sum([item.item_total_price for item in items])
        return total

    class Meta:
        ordering = ['-created']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_items')
    order_time = models.TimeField(default=datetime.datetime.now())
    quantity = models.IntegerField(default=1)
    ignore_ingredient = models.TextField(default='')

    @property
    def item_total_price(self):
        total = self.product.price * self.quantity
        return total
