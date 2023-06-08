import django_filters
from django import forms
from django_filters import LookupChoiceFilter
from django_property_filter import PropertyBooleanFilter
from django_property_filter import PropertyFilterSet
from django_property_filter import PropertyOrderingFilter

from app_product.models import PropertyName
from app_product.models import PropertyValue
from utils.check_model import check_model
from .utils import *
from .widgets import ShopCheckboxInput
from .widgets import ShopLinkWidget


class ProductFilter(PropertyFilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input form-input_full',
                'placeholder': 'Название'
            }
        )
    )
    is_stock = PropertyBooleanFilter(
        field_name='is_stock',
        widget=ShopCheckboxInput
    )
    is_limited = PropertyBooleanFilter(
        field_name='limited_edition',
        widget=ShopCheckboxInput
    )
    product_property = LookupChoiceFilter(
        field_name='product_property__property__name',
        lookup_choices=[
            (property_name, property_name) for property_name in PropertyName.objects.all()
        ] if db_table_exists('product_properties') else []
    )
    product_values = LookupChoiceFilter(
        field_name='product_property__value__value',
        lookup_choices=[
            (property_value, property_value) for property_value in PropertyValue.objects.all()
        ] if db_table_exists('property_value') else []
    )
    
    price = django_filters.CharFilter(
        method='price_range',
        field_name='price',
        lookup_expr='range',
        widget=forms.TextInput(
            attrs={
                'class': 'range-line',
                'data-type': 'double',
                'data-min': get_range_price()['min_price'],
                'data-max': get_range_price()['min_price']
            }
        )
    )
    
    order_by_field = 'ordering'
    ordering = PropertyOrderingFilter(
        choices=(
            ('price', 'Цене'), ('-price', 'Цене'),
            ('add_at', 'Новизне'), ('-add_at', 'Новизне'),
            ('sold_amount', 'Популярности'), ('-sold_amount', 'Популярности'),
            ('total_review', 'Отзывам'), ('-total_review', 'Отзывам')
        ),
        fields=['price', 'add_at', 'sold_amount', 'total_review'],
        empty_label=None,
        widget=ShopLinkWidget
    )
    
    @staticmethod
    def price_range(queryset, _, value):
        return queryset.filter(price__range=value.split(';'))
    
    class Meta:
        model = Product
        order_by_field = 'price'
        fields = ('price', 'title', 'is_stock', 'is_limited')
