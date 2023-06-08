import os

from django.core.management.base import BaseCommand
from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger

from app_users.models import User

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()
    logger.success('Настройки успешно импортированы')


class Command(BaseCommand):
    def handle(self, **options):
        superadmin_name = os.getenv('ADMIN_EMAIL', 'admin@admin.ru')
        superadmin_password = os.getenv('ADMIN_PASSWORD', 'admin')
        
        if not User.objects.filter(email=superadmin_name).first():
            User.objects.create_superuser(
                email=superadmin_name,
                password=superadmin_password)
            logger.success(
                "Superuser created:"
                f"\nName: {superadmin_name}"
                f"\nPassword: {superadmin_password}"
            )
