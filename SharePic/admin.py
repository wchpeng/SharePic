# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.contrib import admin
from django.conf import settings
from django.forms.boundfield import BoundField
from django.forms.models import ModelChoiceField

# 配置 admin.site 的一些自定义信息

admin.site.site_title = "后台管理"
admin.site.site_header = "粉刷匠"
admin.site.index_title = "pic"
admin.site.site_url = "/"  # 配置网站主页
admin.site._registry = OrderedDict()  # 把 _registry 变成 OrderedDict，后面作为注册对象的排序依据


class MyselfInfoList(admin.ModelAdmin):
    # 抽象一个基类，用于创建的时候 creater_id 是当前用户id， 列表数据只显示当前用户创建的数据

    exclude = ["creater", "creater_id"]
    list_display = ['id', '__str__']
    # def get_queryset(self, request):
    #     qs = super(MyselfInfoList, self).get_queryset(request)
    #     return qs.filter(creater_id=request.user.id)

    def save_form(self, request, form, change):
        form.instance.creater_id = request.user.id
        return form.save(commit=False)

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     # 处理返回模版的上下文中的各个（外键）字段的 queryset，过滤出当前用户创建的数据
    #     resp = super(MyselfInfoList, self).change_view(request, object_id, form_url, extra_context)
    #     context_data = resp.context_data
    #     adminform = context_data['adminform']
    #     for fieldsets in adminform:
    #         for line in fieldsets:
    #             for field in line:
    #                 if isinstance(field.field, BoundField) and isinstance(field.field.field, ModelChoiceField):
    #                     field.field.field.queryset = field.field.field.queryset.filter(creater_id=request.user.id)
    #
    #     return resp


def sort_for_model_and_label(template_response):
    context_data = template_response.context_data
    app_list = context_data.get("app_list", [])
    installed_apps_labels = [app.split(".")[-1] for app in settings.INSTALLED_APPS]

    app_list.sort(key=lambda x: installed_apps_labels.index(x["app_label"]))
    registry_apps = [model._meta.verbose_name_plural for model in admin.site._registry]  # 注册的 model 的 name 列表（有序）

    for app in app_list:
        # model 根据 register 时的顺序排
        app["models"].sort(key=lambda x: registry_apps.index(x["name"]))
    return template_response


def sort_for_model_and_label_decorator(func):
    # 写一个装饰器给返回的 app_label/app_model 拍序
    def inner(*args, **kwargs):
        return sort_for_model_and_label(func(*args, **kwargs))
    return inner


# 给返回的 app_model/app_label 拍序：按照注册的顺序, 装饰给 index
admin.site.index = sort_for_model_and_label_decorator(admin.site.index)
# 给返回的 app_model 拍序，按照注册的顺序,装饰给 app_index
admin.site.app_index = sort_for_model_and_label_decorator(admin.site.app_index)

