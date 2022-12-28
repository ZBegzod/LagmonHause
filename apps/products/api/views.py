from rest_framework import status
from django.utils import timezone
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework import mixins, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from apps.products.api.permissions import (
    IsCustomerOfOrder,
    ManagerPermission,
    IsCustomerOfBooking,
    CustomerCancellOrderPermission,
    ManagerCancellAcceptOrderPermission,
)

from apps.products.models import (
    Category,
    Booking,
    Product,
    Order,
    Room,
)

from .serializers import (
    RoomModelSerializer,
    ProductModelSerializer,
    BookingModelSerializer,
    BookingEventSerializer,
    CategoryModelSerializer,
    OrderEventModelSerializer,
    AdminOrderModelSerializer,
    CustomOrderModelSerializer,
    CancellOrderModelSerializer,
    DeliverOrderModelSerializer,
    ProductEventModelSerializer,
    CustomBookingModelSerializer,
    CategoryEventModelSerializer,
    PrepareTimeOrderModelSerializer,

)


# category list and retrieve view all user
class CategoryApiViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = CategoryModelSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        query = Category.objects.filter(status=True)
        return query


# category events view for admin user
class CategoryEventApiViewSet(mixins.CreateModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    serializer_class = CategoryEventModelSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [
        IsAuthenticated,
        ManagerPermission
    ]

    def get_queryset(self):
        query = Category.objects.filter(status=True)
        return query


# product list and retrieve view for all user
class ProductApiViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = ProductModelSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        query = Product.objects.filter(status=True)
        return query


# product events view for admin user
class ProductEventApiViewSet(mixins.CreateModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    permission_classes = [
        IsAuthenticated,
        ManagerPermission
    ]
    serializer_class = ProductEventModelSerializer

    def get_queryset(self):
        query = Product.objects.filter(status=True)
        return query


# room list and retrieve view for all user
class RoomApiViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomModelSerializer
    permission_classes = [AllowAny]


# room events view for admin user
class RoomEventApiViewSet(mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomModelSerializer
    permission_classes = [
        IsAuthenticated,
        ManagerPermission
    ]


# booking list and retrieve view for admin user
class BookingApiViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    permission_classes = [
        IsAuthenticated,
        ManagerPermission
    ]


# booked date own user of booking
class CustomBookingApiViewSet(mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):
    serializer_class = CustomBookingModelSerializer
    permission_classes = [
        IsAuthenticated,
        IsCustomerOfBooking
    ]

    def get_queryset(self):
        query = Booking.objects.filter(guest=self.request.user.pk)
        return query


# booking event for admin user
class BookingEventApiViewSet(mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingEventSerializer
    permission_classes = [
        IsAuthenticated,
        ManagerPermission
    ]


# booking create view for all user
class BookingCreateApiViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    serializer_class = BookingEventSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        room_data = serializer.validated_data.get('room', None)
        room = Room.objects.get(id=room_data.id)
        if room is not None and room.is_booked is False:
            if room.booking is True:
                room.is_booked = True
                room.save()
                serializer.save(guest=request.user)
            else:
                raise ValidationError('Today we are not working!')
        else:
            raise ValidationError('This room is booked please choose an other room!')
        return Response(data={'data': serializer.data, 'message': 'chosen room is booked'},
                        status=status.HTTP_201_CREATED)


# create order for all user
class OderCreateAPIViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderEventModelSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# order prepare time for admin user
class OrderTimeAPIViewSet(mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = PrepareTimeOrderModelSerializer
    permission_classes = [
        ManagerPermission,
        IsAuthenticated,
    ]

    def get_queryset(self):
        query = Order.objects.filter(is_cancelled=False, is_delivered=False)
        return query


# custom cancell own order view
class OrderCancellCustomerAPIViewSet(mixins.UpdateModelMixin,
                                     viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = CancellOrderModelSerializer
    permission_classes = [
        IsAuthenticated,
        IsCustomerOfOrder,
        CustomerCancellOrderPermission
    ]

    def perform_update(self, serializer):
        serializer.save(cancell_datetime=timezone.now())


# custom cancell order list view for own order user
class OrderCustomerCancelledListAPIViewSet(mixins.ListModelMixin,
                                           mixins.RetrieveModelMixin,
                                           viewsets.GenericViewSet):
    serializer_class = CustomOrderModelSerializer
    permission_classes = [
        IsAuthenticated,
        IsCustomerOfOrder
    ]

    def get_queryset(self):
        query = Order.objects.filter(user=self.request.user.pk, is_cancelled=True)
        return query


# all cancelled list order for admin user
class OrderCancellListAdminAPIViewSet(mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin,
                                      mixins.DestroyModelMixin,
                                      viewsets.GenericViewSet):
    serializer_class = AdminOrderModelSerializer
    permission_classes = [
        IsAuthenticated,
        ManagerPermission,
    ]

    def get_queryset(self):
        query = Order.objects.filter(is_cancelled=True)
        return query


# order cancell for admin user
class OrderCancellAdminAPIViewSet(mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):
    serializer_class = CancellOrderModelSerializer
    queryset = Order.objects.all()
    permission_classes = [
        IsAuthenticated,
        ManagerPermission,
        ManagerCancellAcceptOrderPermission
    ]

    def perform_update(self, serializer):
        serializer.save(cancell_datetime=timezone.now())


# order to deliver view for admin user
class OrderDeliverAdminAPIViewSet(mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):
    serializer_class = DeliverOrderModelSerializer
    queryset = Order.objects.all()
    permission_classes = [
        IsAuthenticated,
        ManagerPermission,
        ManagerCancellAcceptOrderPermission
    ]

    def perform_update(self, serializer):
        serializer.save(delivered_datetime=timezone.now())


# all delivered list of order for admin user
class OrderDeliverListAdminAPIViewSet(mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin,
                                      mixins.DestroyModelMixin,
                                      viewsets.GenericViewSet):
    serializer_class = AdminOrderModelSerializer
    permission_classes = [
        IsAuthenticated,
        ManagerPermission
    ]

    def get_queryset(self):
        query = Order.objects.filter(is_delivered=True)
        return query


# all active list order for admin user
class OrderActiveAdminAPIViewSet(mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 viewsets.GenericViewSet):
    serializer_class = AdminOrderModelSerializer
    permission_classes = [
        IsAuthenticated,
        ManagerPermission,
    ]

    def get_queryset(self):
        query = Order.objects.filter(is_cancelled=False, is_delivered=False)
        return query


# active order list view for own order user
class OrderActiveCustomerListAPIViewSet(mixins.ListModelMixin,
                                        mixins.RetrieveModelMixin,
                                        viewsets.GenericViewSet):
    serializer_class = CustomOrderModelSerializer
    permission_classes = [
        IsAuthenticated,
        IsCustomerOfOrder
    ]

    def get_queryset(self):
        query = Order.objects.filter(
            user=self.request.user.pk, is_cancelled=False, is_delivered=False
        )
        return query
