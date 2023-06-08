from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_product'
    verbose_name = _('Приложение «Товар»')
