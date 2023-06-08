from django import forms
from django.utils.translation import gettext_lazy as _


class OrderUserForm(forms.Form):
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
