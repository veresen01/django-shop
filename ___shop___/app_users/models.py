from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from app_settings.models import SiteSettings
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    image_validator = FileExtensionValidator(
        allowed_extensions=['png', 'jpg', 'gif', 'jpeg'],
        message=_('Расширение не поддерживается. Разрешенные расширения .jpg .gif .png .jpeg')
    )
    
    def validate_image_size(fieldfile_obj):
        settings: SiteSettings = SiteSettings.objects.all().first()
        megabyte_limit = settings.avatar_image_max_size_mb
        filesize = fieldfile_obj.file.size
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError(
                _("Вы не можете загрузить аватар размером > {} MB").format(settings.avatar_image_max_size_mb)
            )
    
    email = models.EmailField(
        unique=True,
        verbose_name='E-mail'
    )
    full_name = models.CharField(
        max_length=254,
        verbose_name=_('Полное имя')
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата регистрации')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Активен')
    )
    avatar_file = models.ImageField(
        verbose_name=_('Аватар'),
        upload_to='images/user_avatars/',
        null=True,
        blank=True,
        validators=[validate_image_size, image_validator]
    )
    phoneNumberRegex = RegexValidator(
        regex=r"^\d{10}$"
    )
    phoneNumber = models.CharField(
        validators=[phoneNumberRegex],
        max_length=10,
        unique=True,
        verbose_name=_('Телефон')
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('Сотрудник')
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return f'{self.email} ({self.full_name})'
    
    class Meta:
        ordering = ['id']
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')
        db_table = 'users'


class ProxyGroups(Group):
    class Meta:
        proxy = True
        verbose_name = _('группа')
        verbose_name_plural = _('группы')
