from django.shortcuts import render
from django.urls import reverse_lazy as reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.base import View, TemplateView
from django.contrib.auth.views import LoginView, LogoutView, login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User


class MyLoginView(LoginView):
    # 登录
    extra_context = {'next': reverse('picture:index')}


class MyLogoutView(LogoutView):
    # 退出登录
    next_page = '/'


class MyRegisterView(TemplateView):
    template_name = "user/register_to_login_middle_page.html"

    # 注册用户
    def post(self, request, *args, **kwargs):
        # 验证是否存在 username
        user_name = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if not all([user_name, password, email]):
            return self.render_to_response({"message": "注册失败！"})
        else:
            User.objects.create_user(
                username=user_name,
                email=email,
                password=password
            )
        return self.render_to_response({"message": "注册成功，跳转登陆中..."})


class UserInfoView(LoginRequiredMixin, View):
    login_url = reverse('user:user_login')

    # 用户信息: /user/info/12/
    def get(self, request, *args, **kwargs):
        return JsonResponse({"code": 0, "msg": "成功", "tips": "暂未开发新功能"})


class MyUserInfoView(LoginRequiredMixin, View):
    login_url = reverse('user:user_login')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('user:user_info', args=[request.user.id]))


class CheckUserOrEmailExist(View):
    
    def get(self, request, *args, **kwargs):
        user_name = request.GET.get("username")
        email = request.GET.get("email")
        if user_name:
            return JsonResponse({"code": 0, "data": {"exist": User.objects.filter(username=user_name).exists()}})
        if email:
            return JsonResponse({"code": 0, "data": {"exist": User.objects.filter(email=email).exists()}})
        return JsonResponse({"code": 101, "msg": "缺少参数"})
