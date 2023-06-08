from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from app_product.models import Product
from app_users.forms import User


class CartDatabase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='user_cart'
    )
    good = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Товар'),
        related_name='cart_product'
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_('Количество товара')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Цена')
    )
    
    def __str__(self):
        return f'Корзина {self.user}'
    
    class Meta:
        verbose_name = _('корзина')
        verbose_name_plural = _('корзины')
