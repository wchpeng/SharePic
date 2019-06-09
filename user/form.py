from django.forms import ModelForm, Form, CharField

from .models import User


class LoginForm(Form):
    username = CharField(max_length=10)