"""___shop___ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n', include('django.conf.urls.i18n')),
    path('', include('app_shop.urls', namespace='shop')),
    path('', include('app_product.urls', namespace='product')),
    path('', include('app_reviews.urls', namespace='reviews')),
    path('', include('app_users.urls', namespace='users')),
    path('', include('app_orders.urls', namespace='orders')),
    path('cart/', include('app_cart.urls', namespace='cart')),
    # path('accounts/', include('django.contrib.auth.urls', namespace='accounts')),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
