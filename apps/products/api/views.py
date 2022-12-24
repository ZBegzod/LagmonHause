from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework import generics, mixins, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated
)

from apps.products.models import (
    Category,
    Booking,
    Product,
    Room
)

from .serializers import (
    RoomModelSerializer,
    ProductModelSerializer,
    BookingModelSerializer,
    BookingEventSerializer,
    CategoryModelSerializer,
    ProductEventModelSerializer,
    CategoryEventModelSerializer,
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

    # permission_classes = [IsAuthenticated, IsAdminUser]

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
    # permission_classes = [IsAuthenticated, IsAdminUser]
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
    # permission_classes = [IsAuthenticated, IsAdminUser]


# booking list and retrieve view for admin user
class BookingApiViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser]


# booking event for admin user
class BookingEventApiViewSet(mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingEventSerializer
    # permission_classes = [IsAuthenticated, IsAuthenticated]


# booking create view for all user
class BookingCreateApiViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    serializer_class = BookingEventSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        room = serializer.data.get('room', None)

        if room is not None and room.is_booked is False:
            if room.booking is True:
                serializer.is_valid(raise_exception=True)
                room.is_booked = True
                room.save()
                serializer.save(guest=request.user)
            else:
                raise ValidationError('Today we are not working!')
        else:
            raise ValidationError('This room is booked please choose an other room!')
        return Response(data={'message': 'chosen room is booked'}, status=status.HTTP_201_CREATED)

