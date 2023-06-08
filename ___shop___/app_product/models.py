from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Min
from django.utils.translation import gettext_lazy as _
# Create your models here.
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from app_product.validators import is_svg
from app_users.models import User


def validate_svg(file):
    if not is_svg(file):
        raise ValidationError("Файл не svg")


class Category(MPTTModel):
    title = models.CharField(
        db_index=True,
        max_length=100,
        verbose_name=_('Название')
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.PROTECT,
        verbose_name=_('Родительская категория'),
        related_name='parent_category',
        blank=True,
        null=True
    )
    # icon_link = models.CharField(
    #     max_length=1000,
    #     verbose_name=_('Ссылка на иконку'),
    #     blank=True,
    #     null=True
    # )
    icon = models.FileField(
        upload_to='images/category_icons',
        blank=True,
        validators=[validate_svg],
        verbose_name=_('Иконка SVG')
    )
    image = models.ImageField(
        blank=True,
        upload_to='images/category_images/',
        verbose_name=_('Изображение')
    )
    # image_link = models.CharField(
    #     max_length=1000,
    #     verbose_name=_('Ссылка на изображение'),
    #     blank=True,
    #     null=True
    # )
    active = models.BooleanField(
        default=True,
        verbose_name=_('Категория активна')
    )
    favourite = models.BooleanField(
        default=False,
        verbose_name=_('Избранное')
    )
    sort_index = models.IntegerField(
        default=0,
        verbose_name=_('Индекс сортировки')
    )
    
    class MPTTMeta:
        order_insertion_by = ['title']
    
    def __str__(self):
        full_path = [self.title]
        k: Category = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        
        return ' -> '.join(full_path[::-1])
    
    def get_min(self):
        price = Product.objects.filter(category_id=self.pk). \
            select_related('category'). \
            values('price'). \
            order_by('price').aggregate(
            Min('price')
        )['price__min']
        return price
    
    class Meta:
        ordering = ['sort_index', 'id']
        verbose_name = _('категория')
        verbose_name_plural = _('категории')
        db_table = 'categories'


class Product(models.Model):
    title = models.CharField(
        max_length=1000,
        verbose_name=_('Название')
    )
    
    category = TreeForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='category',
        verbose_name=_('Категория')
    )
    
    description = models.TextField(
        max_length=2000,
        verbose_name=_('Описание'),
        blank=True
    )
    
    description_detailed = models.TextField(
        max_length=5000,
        verbose_name=_('Подробное описание'),
        blank=True
    )
    
    price = models.FloatField(
        verbose_name=_('Цена'),
        default=0
    )
    
    remains = models.IntegerField(
        verbose_name=_('Остаток'),
        default=0
    )
    
    active = models.BooleanField(
        verbose_name=_('Активный товар'),
        default=True
    )
    
    sorting_index = models.IntegerField(
        verbose_name=_('Индекс сортировки'),
        default=0
    )
    
    limited_edition = models.BooleanField(
        verbose_name=_('Ограниченный тираж'),
        default=False
    )
    
    sold_amount = models.IntegerField(
        verbose_name=_('Количество покупок'),
        default=0
    )
    
    add_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата добавления'),
        blank=True,
        null=True
    )
    
    options = models.ManyToManyField(
        'PropertyName',
        through="Property"
    )
    #
    attributes = models.ManyToManyField(
        'AttributeName',
        through="Attribute"
    )
    
    @property
    def total_review(self):
        return len(self.product_comments.all())
    
    @property
    def is_stock(self):
        return self.remains > 0
    
    def __str__(self):
        return f'{self.title} - {self.price}$'
    
    class Meta:
        ordering = ['-sold_amount']
        verbose_name = _('товар')
        verbose_name_plural = _('товары')
        db_table = 'products'


class ProductImages(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        verbose_name=_('Товар'),
        related_name='product_image'
    )
    image = models.ImageField(
        verbose_name=_('Изображение товара'),
        upload_to='images/products/',
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f'img of {self.product.title}'
    
    class Meta:
        ordering = ['id']
        verbose_name = _('изображение')
        verbose_name_plural = _('изображения')
        db_table = 'product_images'


class Property(models.Model):
    property = models.ForeignKey(
        'PropertyName',
        on_delete=models.CASCADE,
        related_name='property',
        verbose_name=_('Характеристика')
    )
    value = models.ForeignKey(
        'PropertyValue',
        on_delete=models.CASCADE,
        verbose_name=_('Значение характеристики')
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        verbose_name=_('Товар'),
        related_name='product_property'
    )


class PropertyName(models.Model):
    name = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=_('Характеристика товара')
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('характеристика')
        verbose_name_plural = _('характеристики')
        db_table = 'product_properties'


class PropertyValue(models.Model):
    value = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=_('Значение характеристики товара')
    )
    
    def __str__(self):
        return self.value
    
    class Meta:
        verbose_name = _('значение')
        verbose_name_plural = _('значения')
        db_table = 'property_value'


class Attribute(models.Model):
    attribute = models.ForeignKey(
        'AttributeName',
        on_delete=models.CASCADE,
        related_name='attributes',
        verbose_name=_('Атрибут товара')
    )
    value = models.ForeignKey(
        'AttributeValue',
        on_delete=models.CASCADE,
        verbose_name=_('Значение атрибута')
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        verbose_name=_('Товар'),
        related_name='product_attributes'
    )


class AttributeName(models.Model):
    name = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=_('Название атрибута')
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('атрибут')
        verbose_name_plural = _('атрибуты')
        db_table = 'attributes'


class AttributeValue(models.Model):
    value = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=_('Значение атрибута товара')
    )
    
    def __str__(self):
        return self.value
    
    class Meta:
        verbose_name = _('значение атрибута')
        verbose_name_plural = _('значения атрибутов')
        db_table = 'attribute_values'


class HistoryProduct(models.Model):
    user = models.ForeignKey(
        User,
        related_name='history_products',
        verbose_name=_('Пользователь'),
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='product',
        verbose_name=_('Товар'),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.product} ({self.user})'

    class Meta:
        verbose_name = _('история просмотра товаров')
        verbose_name_plural = _('истории просмотра товаров')
        db_table = 'history_products'
