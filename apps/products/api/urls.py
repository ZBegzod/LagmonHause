from django.urls import path
from rest_framework import routers
from .views import (
    BookingEventApiViewSet,
    CategoryEventApiViewSet,
    BookingCreateApiViewSet,
    ProductEventApiViewSet,
    RoomEventApiViewSet,
    CategoryApiViewSet,
    BookingApiViewSet,
    ProductApiViewSet,
    RoomApiViewSet,
)

router = routers.DefaultRouter()

# products
router.register(r'products', ProductApiViewSet, basename='products')
router.register(r'product-event', ProductEventApiViewSet, basename='product-event')

# categories
router.register(r'categories', CategoryApiViewSet, basename='categories')
router.register(r'category-event', CategoryEventApiViewSet, basename='category-event')

# rooms
router.register(r'rooms', RoomApiViewSet, basename='rooms')
router.register(r'room-event', RoomEventApiViewSet, basename='room-event')

# reservations
router.register(r'reservations', BookingApiViewSet, basename='reservations')
router.register(r'reservation-create', BookingCreateApiViewSet, basename='reservation-create')
router.register(r'reservation-event', BookingEventApiViewSet, basename='reservation-event')

urlpatterns = router.urls
