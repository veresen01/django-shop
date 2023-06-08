from django.db import OperationalError
from loguru import logger

from app_settings.models import SiteSettings


def settings_context(request):
    context = dict()
    try:
        settings: SiteSettings = SiteSettings.objects.all().first()
    except OperationalError:
        logger.error('SETTINGS ERROR')
    else:
        logger.success('SETTINGS GOT')
        context['settings'] = settings
    
    return context
