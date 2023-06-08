from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from app_product.models import Product
from app_users.models import User


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviewer',
        verbose_name=_('Пользователь')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_comments',
        verbose_name=_('Товар')
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    text = models.TextField(
        blank=False,
        verbose_name=_('Текст отзыва'),
        max_length=2000
    )
    
    def __str__(self):
        return f'[{self.user.email}] - {self.create_at.strftime("%Y-%m-%d %H:%M:%S")}'
    
    class Meta:
        ordering = ['-create_at']
        verbose_name = _('комментарий')
        verbose_name_plural = _('комментарии')
        db_table = 'comments'
