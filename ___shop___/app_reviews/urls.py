from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

app_name = 'reviews'

urlpatterns = [
    path(
        'reviews/add',
        AddReview.as_view(),
        name='add'
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
