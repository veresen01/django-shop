# Register your models here.
from django.contrib import admin

from .models import *


class OrderItemsTabularInline(admin.TabularInline):
    """
    Админка редактирования заказа с привязкой товаров
    """
    model = OrderItems


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'create_at',
        'method_payment',
        'method_delivery',
        'payment_status',
        'payment_at',
    ]
    list_display_links = ['user']
    inlines = [OrderItemsTabularInline]


@admin.register(PaymentStatuses)
class PaymentStatusesAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'priority'
    ]
    list_display_links = ['title']


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title'
    ]
    list_display_links = ['title']


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'description'
    ]
    list_display_links = ['title']
