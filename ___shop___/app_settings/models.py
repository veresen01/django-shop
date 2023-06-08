from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class SingletonModel(models.Model):
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        pass
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    order_delivery_limit = models.IntegerField(
        default=2000,
        verbose_name=_('Лимит суммы для бесплатной доставки')
    )
    order_delivery_price = models.IntegerField(
        default=200,
        verbose_name=_('Стоимость доставки')
    )
    order_delivery_express = models.IntegerField(
        default=500,
        verbose_name=_('Стоимость экспресс-доставки')
    )
    access_to_auth_when_auth = models.BooleanField(
        default=True,
        verbose_name=_('Доступ к аутентификации, когда авторизован')
    )
    avatar_image_max_size_mb = models.FloatField(
        default=2,
        verbose_name=_('Максимальный размер аватарки, МБ')
    )
    popular_product_amount = models.IntegerField(
        default=8,
        verbose_name=_('Количество популярных товаров на главной')
    )
    product_page_amount = models.IntegerField(
        default=2,
        verbose_name=_('Количество товаров на странице')
    )
    
    class Meta:
        verbose_name = _('настройка сайта')
        verbose_name_plural = _('настройки сайта')
        db_table = 'settings'
