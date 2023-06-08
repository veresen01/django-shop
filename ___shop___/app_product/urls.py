from django.urls import path

from .views import *

app_name = 'product'

urlpatterns = [
    path(
        'product/<int:pk>',
        ProductDetailView.as_view(),
        name='product_detail'
    ),
]
