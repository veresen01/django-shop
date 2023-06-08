from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

app_name = 'orders'

urlpatterns = [
    path(
        'order/',
        OrderView.as_view(),
        name='order_step_1'
    ),
    path(
        'order/<int:pk>',
        OrderDetail.as_view(),
        name='order_detail'
    ),
    path(
        'order/<int:pk>/payment',
        OrderDetailPayment.as_view(),
        name='order_detail_payment'
    ),
    path(
        'order/process',
        OrderPaymentProcess.as_view(),
        name='order_payment_process'
    ),
    path(
        'create-order/',  # ajax
        create_order,
        name='create_order'
    ),
    path(
        'cancel-order/',  # ajax
        cancel_order,
        name='cancel_order'
    ),
    path(
        'order-canceled/',  # ajax
        OrderCancelView.as_view(),
        name='order_canceled'
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
