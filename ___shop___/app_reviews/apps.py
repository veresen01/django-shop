from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_reviews'
    verbose_name = _('Приложение «Отзывы»')
