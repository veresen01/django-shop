from django.contrib import admin

# Register your models here.
from app_product.models import Attribute
from app_product.models import AttributeName
from app_product.models import AttributeValue
from app_product.models import Category
from app_product.models import HistoryProduct
from app_product.models import Product
from app_product.models import ProductImages
from app_product.models import Property
from app_product.models import PropertyName
from app_product.models import PropertyValue
from app_reviews.models import Review


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in ProductImages._meta.get_fields()
    ]


@admin.register(HistoryProduct)
class HistoryProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'product'
    ]


class ReviewsTabularInline(admin.TabularInline):
    """
    Админка редактирования товара с привязкой отзывов
    """
    model = Review


class PropertyTabularInline(admin.TabularInline):
    """
    Админка редактирования товара с привязкой характеристик
    """
    model = Property


class AttributesTabularInline(admin.TabularInline):
    """
    Админка редактирования товара с привязкой характеристик
    """
    model = Attribute


class ProductImagesTabularInline(admin.TabularInline):
    """
    Админка редактирования товара с привязкой изображений
    """
    model = ProductImages


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'sort_index',
        'title',
        'parent',
        'icon',
        'image',
        'favourite',
        'active'
    ]
    list_display_links = ['title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'category',
        'description',
        'price',
        'remains',
        'sorting_index',
        'limited_edition',
        'sold_amount',
        'active',
        'add_at',
    ]
    list_display_links = ['title']
    inlines = [
        ProductImagesTabularInline,
        PropertyTabularInline,
        AttributesTabularInline,
        ReviewsTabularInline
    ]


@admin.register(PropertyName)
class PropertyNameAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name'
    ]
    list_display_links = ['name']


@admin.register(PropertyValue)
class PropertyValueAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'value'
    ]
    list_display_links = ['value']


@admin.register(AttributeName)
class AttributeNameAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name'
    ]
    list_display_links = ['name']


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'value'
    ]
    list_display_links = ['value']
