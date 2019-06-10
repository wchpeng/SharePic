from django.shortcuts import render
from django.urls import reverse_lazy as reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.base import View, TemplateView
from django.contrib.auth.views import LoginView, LogoutView, login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
            return HttpResponseRedirect(reverse('user:user_login'))
        else:
            User.objects.create_user(
                username=user_name,
                email=email,
                password=password
            )
        return HttpResponseRedirect(reverse('user:user_login'))


class UserInfoView(LoginRequiredMixin, View):
    login_url = reverse('user:user_login')

    # 用户信息: /user/info/12/
    def get(self, request, *args, **kwargs):
        return JsonResponse({"code": 0, "msg": "成功", "tips": "暂未开发新功能"})


class MyUserInfoView(LoginRequiredMixin, View):
    login_url = reverse('user:user_login')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('user:user_info', args=[request.user.id]))
