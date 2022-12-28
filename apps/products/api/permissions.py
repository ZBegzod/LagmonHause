from rest_framework import permissions
from apps.products.models import Order, Booking


class ManagerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user.is_manager


class CustomerCancellOrderPermission(permissions.BasePermission):
    message = (
        "You do not have permission to cancell this order"
    )

    def has_permission(self, request, view):
        order = Order.objects.filter(id=view.kwargs.get("pk", None)).first()
        if order is None:
            return False
        return not order.is_delivered and not order.is_cancelled


class IsCustomerOfOrder(permissions.BasePermission):
    message = (
        "You can't cancell this order because you are not it's owner."
    )

    def has_permission(self, request, view):
        order = Order.objects.filter(user=request.user.pk).first()
        return order is not None


class IsCustomerOfBooking(permissions.BasePermission):
    message = (
        "You can't view this booking date because you are not it's owner."
    )

    def has_permission(self, request, view):
        booking = Booking.objects.filter(guest=request.user.pk).first()
        return booking is not None


class ManagerCancellAcceptOrderPermission(permissions.BasePermission):
    message = "You don't have permission to cancell this order."

    def has_permission(self, request, view):
        order = Order.objects.filter(pk=view.kwargs.get("pk", None)).first()
        if order is None:
            return False
        return not order.is_cancelled and not order.is_delivered
