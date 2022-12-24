from django.contrib import admin
from apps.products.models import (
    Room,
    Order,
    Booking,
    Product,
    Category,
    OrderItem,
    RoomImages,
    ProductImages,
)

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Booking)
admin.site.register(ProductImages)
admin.site.register(Room)
admin.site.register(RoomImages)
admin.site.register(Order)
admin.site.register(OrderItem)

