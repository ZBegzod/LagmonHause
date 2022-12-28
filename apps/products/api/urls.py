from .views import (
    CategoryApiViewSet,
    CategoryEventApiViewSet,

    BookingApiViewSet,
    BookingEventApiViewSet,
    BookingCreateApiViewSet,
    CustomBookingApiViewSet,

    RoomApiViewSet,
    ProductApiViewSet,
    RoomEventApiViewSet,
    ProductEventApiViewSet,

    OderCreateAPIViewSet,
    OrderCancellCustomerAPIViewSet,
    OrderActiveCustomerListAPIViewSet,
    OrderCustomerCancelledListAPIViewSet,

    OrderTimeAPIViewSet,
    OrderActiveAdminAPIViewSet,

    OrderDeliverAdminAPIViewSet,
    OrderDeliverListAdminAPIViewSet,

    OrderCancellAdminAPIViewSet,
    OrderCancellListAdminAPIViewSet,

)
from django.urls import path
from rest_framework import routers

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
router.register(r'reservations-admin', BookingApiViewSet, basename='reservations')
router.register(r'reservations-customer', BookingApiViewSet, basename='reservations')
router.register(r'reservation-create', BookingCreateApiViewSet, basename='reservation-create')
router.register(r'reservation-event', BookingEventApiViewSet, basename='reservation-event')

# order
router.register(r'customer-order-create', OderCreateAPIViewSet, basename='customer-order-create')
router.register(r'customer-active-orders', OrderActiveCustomerListAPIViewSet, basename='customer-active-orders')
router.register(r'customer-cancel-order', OrderCancellCustomerAPIViewSet, basename='customer-cancel-order')
router.register(r'custom-cancel-order-list', OrderCustomerCancelledListAPIViewSet, basename='custom-cancel-order-list')

router.register(r'admin-order-time', OrderTimeAPIViewSet, basename='admin-order-time')
router.register(r'admin-active-orders', OrderActiveAdminAPIViewSet, basename='admin-active-orders')

router.register(r'admin-deliver', OrderDeliverAdminAPIViewSet, basename='admin-order-deliver')
router.register(r'admin-order-deliver-list', OrderDeliverListAdminAPIViewSet, basename='admin-order-deliver-list')

router.register(r'admin-order-cancel', OrderCancellAdminAPIViewSet, basename='admin-order-cancel')
router.register(r'admin-order-cancel-list', OrderCancellListAdminAPIViewSet, basename='admin-order-cancel-list')

urlpatterns = router.urls
