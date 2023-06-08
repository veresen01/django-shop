from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppTagsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_tags'
    verbose_name = _('Приложение «Пользовательские теги»')
