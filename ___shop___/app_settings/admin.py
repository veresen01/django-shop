from django.contrib import admin


# Register your models here.
from loguru import logger

from app_settings.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in SiteSettings._meta.get_fields()
    ]
    list_display_links = [
        field.name for field in SiteSettings._meta.get_fields()
    ]
    
    # def __init__(self, model, admin_site):
    #     super().__init__(model, admin_site)
    #     fields: list = [field.name for field in SiteSettings._meta.get_fields()]
    #     logger.debug(fields)
