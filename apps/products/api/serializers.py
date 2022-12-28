from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.core.exceptions import ValidationError
from apps.accounts.models import UserProfile
from rest_framework import serializers
from apps.products.models import (
    ProductImages, Product,
    RoomImages, Room,
    OrderItem, Order,
    Category, Booking,
)


# product images serializer
class ProductImagesModelSerializer(serializers.ModelSerializer):
    image = serializers.CharField()

    class Meta:
        model = ProductImages
        fields = ['image']


# product list and retrieve serializer
class ProductModelSerializer(serializers.ModelSerializer):
    product_images = ProductImagesModelSerializer(many=True)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'product_images',
            'category',
            'name',
            'price',
            'created',
            'updated',
            'description'
        ]


# product events serializer
class ProductEventModelSerializer(WritableNestedModelSerializer):
    product_images = ProductImagesModelSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'product_images',
            'category',
            'name',
            'price',
            'description',
            'status'
        ]

    def create(self, validated_data):
        product_items = validated_data.pop('product_images')
        product = Product.objects.create(**validated_data)

        for product_item in product_items:
            ProductImages.objects.create(product=product, **product_item)

        return product

    def update(self, instance, validated_data):
        product_images_data = validated_data.pop('product_images')

        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.available_inventory = validated_data.get('available_inventory', instance.available_inventory)
        instance.status = validated_data.get('status', instance.status)

        instance.save()

        for product_image_data in product_images_data:
            if not ('id' in product_image_data):
                ProductImages.objects.create(product=instance, **product_image_data)
            else:
                product_image = ProductImages.objects.get(id=product_image_data['id'])
                product_image.image = product_image_data.get('image', product_image.image)
                product_image.save()

        return instance


# categories list and retrieve serializer
class CategoryModelSerializer(serializers.ModelSerializer):
    category_product = ProductModelSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'category_product']


# category events serializer
class CategoryEventModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'image']


# room images serializer
class RoomImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(required=False)

    class Meta:
        model = RoomImages
        fields = ['image']


# room events and list retrieve serializer
class RoomModelSerializer(serializers.ModelSerializer):
    room_images = RoomImageSerializer(many=True)

    # room_images = serializers.SerializerMethodField()
    # def room_images(self, room):
    # return RoomImageSerializer(room.room_images.all(), many=True).data

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'room_images',
            'room_number',
            'room_capacity',
            'price',
            'booking',
            'is_booked'
        ]

    def create(self, validated_data):
        room_items = validated_data.pop('room_images')
        room = Room.objects.create(**validated_data)

        for room_item in room_items:
            RoomImages.objects.create(room=room, **room_item)

        return room

    def update(self, instance, validated_data):
        room_images_data = validated_data.pop('room_images')

        instance.name = validated_data.get('name', instance.name)
        instance.room_number = validated_data.get('room_number', instance.room_number)
        instance.room_capacity = validated_data.get('room_capacity', instance.room_capacity)
        instance.price = validated_data.get('price', instance.price)
        instance.booking = validated_data.get('booking', instance.booking)
        instance.is_booked = validated_data.get('is_booked', instance.is_booked)

        instance.save()

        for room_image_data in room_images_data:

            if not ('id' in room_image_data):
                RoomImages.objects.create(room=instance, **room_image_data)
            else:
                images = RoomImages.objects.get(pk=room_image_data['id'])
                images.image = room_image_data.get('image', images.image)
                images.save()

        return instance


# custom list serializer
class CustomModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['email', 'phone_number', 'get_full_name']


# booking list and retrieve serializer
class BookingModelSerializer(serializers.ModelSerializer):
    room = RoomModelSerializer(read_only=True)
    guest = CustomModelSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'guest', 'room', 'reservation_date',
            'number_of_guest', 'created', 'updated'
        ]


class CustomBookingModelSerializer(serializers.ModelSerializer):
    room = RoomModelSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'room',
            'reservation_date',
            'number_of_guest',
        ]


# booking create serializer for all user
class BookingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['room', 'reservation_date', 'number_of_guest']

    def validate(self, attrs):
        number_of_guest = attrs['number_of_guest']
        room = attrs['room']

        if number_of_guest > room.room_capacity:
            raise ValidationError('Number of guests more than from room capacity!')

        return attrs

    def update(self, instance, validated_data):
        instance.room = validated_data.get('room', instance.room)
        instance.reservation_date = validated_data.get('reservation_date', instance.reservation_date)

        number_of_guest = validated_data.get('number_of_guest')
        room = validated_data.get('room')

        if number_of_guest > room.room_capacity:
            raise ValidationError('Number of guests more than from room capacity!')

        if room.is_booked:
            raise ValidationError('This room is booked please choose an other room!')

        if room.booking is False:
            raise ValidationError('This room is disable!')

        instance.number_of_guest = validated_data.get('number_of_guest', instance.number_of_guest)
        room.is_booked = True
        room.save()

        instance.save()

        return instance


class OrderItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'product',
            'quantity',
            'ignore_ingredient',
        ]


# order  serializer for all user
class OrderEventModelSerializer(serializers.ModelSerializer):
    order_items = OrderItemModelSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'order_items',
            'order_address'
        ]

    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        request = self.context.get('request')
        order = Order.objects.create(**validated_data)

        for order_item in order_items:
            OrderItem.objects.create(order=order, **order_item)

        return order


# order item list and retrieve for all user
class CustomOrderItemModelSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'product', 'item_total_price',
            'quantity', 'ignore_ingredient'
        ]


# order list and retrieve for all user
class CustomOrderModelSerializer(serializers.ModelSerializer):
    order_items = OrderItemModelSerializer(read_only=True, many=True)

    # user = CustomModelSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'order_address',
            'is_cancelled',
            'created', 'status',
            'prepared_time',
            'cancell_datetime',
            'order_items',
            'order_total_price'
        ]


class AdminOrderModelSerializer(serializers.ModelSerializer):
    order_items = OrderItemModelSerializer(read_only=True, many=True)
    user = CustomModelSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'user',
            'order_address',
            'is_delivered',
            'is_cancelled',
            'created', 'status',
            'prepared_time',
            'cancell_datetime',
            'delivered_datetime',
            'order_items',
            'order_total_price'
        ]


# cancell order for user own order serializer
class CancellOrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['is_cancelled']


# order deliver serializer for admin user
class DeliverOrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['is_delivered']


# order prepared_time serializer for admin user
class PrepareTimeOrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['prepared_time']
