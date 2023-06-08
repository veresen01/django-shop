# Create your views here.
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django_filters.views import FilterView

from app_product.models import Category
from app_product.models import Product
from app_settings.models import SiteSettings
from app_shop.filters import ProductFilter
from app_shop.utils import get_range_price

granted_sorts = (
    'sold_amount',  # популярности
    'add_at',  # новизне
    'price',  # цене
    'product_comments',  # количеству отзывов
)
granted_sort_dirs = (
    '',
    '-'
)


class ShopIndexView(generic.TemplateView):
    template_name = 'pages/shop/shop.html'
    page_description = _('Главная страница магазина')
    
    def get_context_data(self, **kwargs):
        settings: SiteSettings = SiteSettings.load()
        
        context = super().get_context_data(**kwargs)
        
        favourite_categories: Category = Category.objects.filter(
            favourite=True
        )
        
        popular_products: Product = Product.objects.filter(active=True).order_by('-sold_amount')[
                                    :settings.popular_product_amount]
        limited_products: Product = Product.objects.filter(
            active=True,
            limited_edition=True
        ).order_by('price')
        
        context['page_description'] = self.page_description
        context['favourite_categories'] = favourite_categories
        context['popular_products'] = popular_products
        context['limited_products'] = limited_products
        return context


class CatalogView(FilterView):
    template_name = 'pages/shop/catalog.html'
    model = Product
    page_title = _('Каталог')
    page_description = _('Каталог товаров')
    context_object_name = 'products_list'
    filterset_class = ProductFilter
    
    category = None
    
    def get(self, request: HttpRequest, *args, **kwargs):
        settings: SiteSettings = SiteSettings.load()
        self.paginate_by = 2
        if settings.product_page_amount:
            self.paginate_by = settings.product_page_amount
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super(CatalogView, self).get_queryset()
        queryset = queryset.filter(
            active=True
        )
        category_id = self.kwargs.get('category_id', 0)
        if category_id:
            self.category: Category = Category.objects.filter(pk=category_id)
            if self.category.exists():
                self.category = self.category.first()
                queryset = queryset.filter(
                    category=self.category
                )
        return queryset
    
    def get_context_data(self, **kwargs):
    
        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
        
        context = super().get_context_data(**kwargs)
        
        context['parameters'] = parameters
        context['page_title'] = self.page_title
        context['page_description'] = self.page_description
        context['section_column'] = " Section_column Section_columnLeft"
        
        price_range = get_range_price(self.category)

        context['filter'].form.fields['price'].widget.attrs = {
            'class': 'range-line',
            'data-type': 'double',
            'data-min': price_range['min_price'],
            'data-max': price_range['max_price']
        }
        
        return context
