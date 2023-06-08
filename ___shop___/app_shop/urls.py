from django.urls import path

from .views import *

app_name = 'shop'

urlpatterns = [
    path(
        '',
        ShopIndexView.as_view(),
        name='index'
    ),
    path(
        'catalog/',
        CatalogView.as_view(),
        name='catalog'
    ),
    path(
        'catalog/<int:category_id>',
        CatalogView.as_view(),
        name='catalog_category'
    ),
    # path(
    #     'catalog/',
    #     ProductByCategoryView.as_view(),
    #     name='catalog'
    # ),
    # path(
    #     'catalog/<int:category_id>',
    #     ProductByCategoryView.as_view(),
    #     name='catalog_category'
    # ),
]
