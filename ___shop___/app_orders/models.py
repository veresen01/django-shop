from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from app_product.models import Product
from app_settings.models import SiteSettings
from app_users.models import User


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_order',
        verbose_name=_('Пользователь')
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    method_payment = models.ForeignKey(
        'PaymentMethod',
        on_delete=models.CASCADE,
        verbose_name=_('Способ оплаты'),
        related_name='method_payment'
    )
    method_delivery = models.ForeignKey(
        'DeliveryMethod',
        on_delete=models.CASCADE,
        verbose_name=_('Способ доставки'),
        related_name='method_delivery'
    )
    payment_status = models.ForeignKey(
        'PaymentStatuses',
        on_delete=models.CASCADE,
        verbose_name=_('Статус оплаты'),
        related_name='payment_status'
    )
    payment_at = models.DateTimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
        verbose_name=_('Дата оплаты')
    )
    city = models.CharField(
        max_length=100,
        verbose_name=_('Город'),
        blank=True
    )
    address = models.CharField(
        max_length=1000,
        verbose_name=_('Адрес'),
        blank=True
    )
    
    def get_total_items(self):
        order_item: OrderItems
        return sum([order_item.product_amount for order_item in self.order.all()])
    
    def get_items(self):
        return self.order.all()
    
    def get_total_price(self):
        items = self.get_items()
        order_item: OrderItems
        return sum([order_item.product_amount * order_item.product_price for order_item in items])
    
    def get_price_with_delivery(self):
        settings: SiteSettings = SiteSettings.load()
        total_price = self.get_total_price()
        if self.method_delivery.id == 1:
            if total_price < settings.order_delivery_limit:
                return total_price + settings.order_delivery_price
            else:
                return total_price
        elif self.method_delivery.id == 2:
            return total_price + settings.order_delivery_express
    
    def get_delivery_price(self):
        settings: SiteSettings = SiteSettings.load()
        total_price = self.get_total_price()
        if self.method_delivery.id == 1:
            if total_price < settings.order_delivery_limit:
                return settings.order_delivery_price
            else:
                return 0
        elif self.method_delivery.id == 2:
            return settings.order_delivery_express
    
    def __str__(self):
        return f'{self.user.email} (от {self.create_at.strftime("%Y-%m-%d %H:%M:%S")}) - {self.payment_status.title}'
    
    class Meta:
        ordering = ['-create_at', '-payment_status', '-payment_at']
        verbose_name = _('заказ')
        verbose_name_plural = _('заказы')
        db_table = 'orders'


class OrderItems(models.Model):
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        verbose_name=_('Заказ'),
        related_name='order'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Товар'),
        related_name='order_product'
    )
    product_amount = models.IntegerField(
        verbose_name=_('Количество товара'),
        default=1
    )
    product_price = models.FloatField(
        verbose_name=_('Цена товара'),
        default=0
    )
    
    def __str__(self):
        return f'[{self.order.id}] {self.product.title} ({self.product_price}$) - {self.product_amount}'
    
    class Meta:
        ordering = ['id']
        verbose_name = _('товар заказа')
        verbose_name_plural = _('товары заказа')
        db_table = 'order_items'


class PaymentMethod(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name=_('Название')
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['id']
        verbose_name = _('способ оплаты')
        verbose_name_plural = _('способы оплаты')
        db_table = 'payment_methods'


class DeliveryMethod(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name=_('Название')
    )
    description = models.TextField(
        max_length=1000,
        verbose_name=_('Описание')
    )
    
    def get_desc(self):
        settings: SiteSettings = SiteSettings.load()
        return _(self.description).format(
            DELIVERY_LIMIT=settings.order_delivery_limit,
            DELIVERY_PRICE=settings.order_delivery_price,
            DELIVERY_EXPRESS_PRICE=settings.order_delivery_express
        )
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['id']
        verbose_name = _('способ доставки')
        verbose_name_plural = _('способы доставки')
        db_table = 'delivery_methods'


class PaymentStatuses(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name=_('Название')
    )
    priority = models.IntegerField(
        verbose_name=_('Приоритет'),
        default=0
    )
    
    def __str__(self):
        return f'{self.title} - {self.priority}'
    
    class Meta:
        ordering = ['-priority']
        verbose_name = _('статус оплаты')
        verbose_name_plural = _('статусы оплаты')
        db_table = 'payment_statuses'
