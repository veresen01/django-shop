from django.urls import path

from .views import *

app_name = 'users'

urlpatterns = [
    path(
        'login/',
        MyLoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        LogOutView.as_view(),
        name='logout'
    ),
    path(
        'signup/',
        SignUpView.as_view(),
        name='signup'
    ),
    path(
        'recovery/',
        RecoveryView.as_view(),
        name='recovery'
    ),
    path(
        'account/',
        AccountView.as_view(),
        name='account'
    ),
    path(
        'profile/',
        ProfileView.as_view(),
        name='profile'
    ),
    path(
        'history-orders/',
        HistoryOrdersListView.as_view(),
        name='history_orders'
    ),
    path(
        'history-product/',
        HistoryProductsListView.as_view(),
        name='history_products'
    ),
]
