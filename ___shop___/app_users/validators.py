import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def clear_phone(phone: str):
    phone = phone.replace('+7', '')
    nums = re.findall(r'\d+', phone)
    nums = [i for i in nums]
    return ''.join(nums)


class PasswordValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'^.*(?=.{8,})(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!#$%&?]).*$', password):
            raise ValidationError(
                _("Пароль должен содержать 8 символов и минимум 1 цифру, одну букву, одну букву в верхнем регистре и один специальный символ из !#$%&?"),
                code='password_invalid'
            )
    
    def get_help_text(self):
        return _(
            "Пароль должен содержать 8 символов и минимум 1 цифру, одну букву, одну букву в верхнем регистре и один специальный символ из !#$%&?")
