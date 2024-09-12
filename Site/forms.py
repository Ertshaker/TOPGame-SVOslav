import re

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from Site.models import Game, Account


def check_username(text):
    if re.search('[\u0400-\u04FF]', text):
        raise forms.ValidationError("Username should not have Cyrillic")
    All_users = Account.objects.all().values_list('username', flat=True)
    if text in All_users:
        raise forms.ValidationError("Username is already taken")


def check_password(password):
    if re.search('[\u0400-\u04FF]', password):
        raise forms.ValidationError("Password should not have Cyrillic")
    if " " in password.strip():
        raise forms.ValidationError("Password should not have space")
    if len(password) < 8:
        raise forms.ValidationError("Password should have at least 8 characters")


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Логин', required=True, max_length=30,
                               widget=forms.TextInput(attrs={'type': 'text', 'class': 'username_field',
                                                             'placeholder': 'Имя пользователя'}),
                               validators=[UnicodeUsernameValidator(), check_username])
    password = forms.CharField(label='Пароль', required=True, max_length=30,
                               widget=forms.PasswordInput(
                                   attrs={'type': 'password', 'class': 'password_field', 'placeholder': 'Пароль'}),
                               validators=[check_password])
    confirm_password = forms.CharField(label='Повторите пароль', required=True, max_length=30,
                                       widget=forms.PasswordInput(
                                           attrs={'type': 'password', 'placeholder': 'Повторите пароль'}))
    email = forms.CharField(label='Email', min_length=3, max_length=30, widget=forms.TextInput(
        attrs={'type': 'email', 'class': 'email_field', 'placeholder': 'Email'}))
    first_name = forms.CharField(label='Имя', max_length=30,
                                 widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', max_length=30,
                                widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Фамилия'}))
    avatar = forms.ImageField(label='Изображение', required=False)


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', required=True, max_length=30,
                               widget=forms.TextInput(
                                   attrs={'type': 'text', 'class': 'form-input', 'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль', required=True, max_length=30,
                               widget=forms.PasswordInput(
                                   attrs={'type': 'password', 'class': 'form-input', 'placeholder': 'Пароль'}))



class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Старый пароль', required=True, max_length=255,
                                   widget=forms.PasswordInput(
                                       attrs={'type': 'password', 'placeholder': 'Старый пароль'}))
    new_password = forms.CharField(label='Новый пароль', required=True, max_length=255,
                                   widget=forms.PasswordInput(
                                       attrs={'type': 'password', 'placeholder': 'Новый пароль'}),
                                   validators=[check_password])


class AddFriendForm(forms.Form):
    friend_name = forms.CharField(label='Имя друга', max_length=30,
                                  widget=forms.TextInput(attrs={'type': 'text'}))


class ChangeAvatarForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ChangeAvatarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'Change_avatar'

    image = forms.ImageField(label='Новый аватар', widget=forms.FileInput(attrs={"id": "image_field"}))
