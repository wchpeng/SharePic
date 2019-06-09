from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import View, TemplateView
from django.contrib.auth.views import LoginView, LogoutView

from .models import User


class MyLoginView(LoginView):
    # 登录
    extra_context = {'next': '/user/info/'}


class MyLogoutView(LogoutView):
    # 退出登录
    next_page = '/'


class MyRegisterView(View):
    # 注册用户
    def post(self, request, *args, **kwargs):
        # 验证是否存在 username
        user_name = request.GET.get("username")
        password = request.GET.get("password")
        email = request.GET.get(password)
        if not all([user_name, password, email]):
            return HttpResponseRedirect(reverse('user:login'))
        else:
            User.objects.create_user(
                username=user_name,
                email=email,
                password=password
            )
        return HttpResponseRedirect(reverse('user:login'))


class UserInfoView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('user:login'))
        pass

# class RegisterOrLogin(TemplateView):
        # template_name = 'user/register_or_login.html'




