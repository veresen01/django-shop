from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class RegForm(UserCreationForm):
    password1 = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'data-validate': 'requirePassword',
                'placeholder': _('Пароль'),
                'autocomplete': 'new-password',
                'maxlength': '150'
            }
        )
    )
    password2 = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'data-validate': 'requireRepeatPassword',
                'placeholder': _('Повторите пароль'),
                'autocomplete': 'new-password',
                'maxlength': '150'
            }
        )
    )
    full_name = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'data-validate': 'require',
                'placeholder': _('Полное имя'),
                'maxlength': '254'
            }
        )
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'data-validate': 'requireMail',
                'placeholder': 'E-mail',
                'maxlength': '254'
            }
        )
    )
    phoneNumber = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'data-validate': 'requirePhone',
                'placeholder': _('Телефон'),
            }
        )
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-input',
                # 'type': "file",
                'accept': ".jpg,.gif,.png,.jpeg",
                'data-validate': "onlyImgAvatar"
            }
        )
    )
    
    class Meta:
        model = User
        fields = (
            'password1',
            'password2',
            'full_name',
            'email',
            'phoneNumber',
            'avatar'
        )


class UpdateProfileForm(forms.Form):
    password1 = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'data-validate': 'requirePassword',
                'placeholder': _('Пароль'),
                'autocomplete': 'new-password',
                'maxlength': '150'
            }
        )
    )
    password2 = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'data-validate': 'requireRepeatPassword',
                'placeholder': _('Повторите пароль'),
                'autocomplete': 'new-password',
                'maxlength': '150'
            }
        )
    )
    full_name = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'data-validate': 'require',
                'placeholder': _('Полное имя'),
                'maxlength': '254'
            }
        )
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'data-validate': 'requireMail',
                'placeholder': 'E-mail',
                'maxlength': '254'
            }
        )
    )
    phoneNumber = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'data-validate': 'requirePhone'
            }
        )
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'Profile-file form-input',
                'type': "file",
                'accept': ".jpg,.gif,.png,.jpeg",
                'data-validate': "onlyImgAvatar"
            }
        )
    )
    
    # class Meta:
    #     model = User
    #     fields = (
    #         'password1',
    #         'password2',
    #         'full_name',
    #         'email',
    #         'phoneNumber',
    #         'avatar'
    #     )


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'data-validate': 'require',
                'maxlength': '254',
                'placeholder': 'E-mail',
                'autocomplete': 'email'
            }
        )
    )
    
    password = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'data-validate': 'require',
                'placeholder': _('Пароль'),
                'autocomplete': 'password',
                'maxlength': '150'
            }
        )
    )


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'data-validate': 'require',
                'maxlength': '254',
                'autocomplete': 'email',
                'placeholder': 'E-mail',
            }
        )
    )


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'data-validate': 'requirePassword',
            'placeholder': _('Пароль'),
            "autocomplete": "new-password",
            'maxlength': '150'
        }),
        strip=False
    )
    new_password2 = forms.CharField(
        max_length=150,
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'data-validate': 'requireRepeatPassword',
            'placeholder': _('Повторите пароль'),
            "autocomplete": "new-password",
            'maxlength': '150'
        }),
    )
