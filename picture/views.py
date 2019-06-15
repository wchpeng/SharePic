from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.core.paginator import Paginator
from django.db.models.query_utils import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as reverse
from django.http import JsonResponse, Http404

from .models import Picture, Album, FavoriteAlbum
from .utils import extend_albums_count, update_favorite_album_count, extend_album_info


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = reverse('user:user_login')
    template_name = "picture/index.html"

    def get_page(self):
        # 获取分页器
        page_no = int(self.request.GET.get("page_no", 1) or 1)
        page_size = int(self.request.GET.get("page_size", 18) or 18)
        if page_size > 50:
            page_size = 18

        return Paginator(self.get_queryset(), page_size).get_page(page_no)

    def get_context_data(self, **kwargs):

        page = self.get_page()
        albums = page.object_list
        values = albums.values("id", "create_time", "title", "desc", "creater_id", "first_picture_id")
        if values:
            extend_albums_count(values, self.request.user.id)  # 扩展收藏数、回复数、用户名、第一张图片

        kwargs["values"] = values
        kwargs["page"] = page
        kwargs["q"] = self.request.GET.get("q", "")

        return kwargs

    def get_queryset(self):
        # 获取查询集
        q = self.request.GET.get("q", "")
        if q:
            return Album.objects.filter(Q(desc__contains=q) | Q(title__contains=q)).order_by("-id")
        return Album.objects.all().order_by("-id")


class AlbumInfoView(LoginRequiredMixin, View):
    login_url = reverse('user:user_login')

    def get(self, request, album_id, *args, **kwargs):
        # 相冊詳情
        try:
            album_info = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            return Http404("沒有改相冊。")

        di = album_info.to_dict(("id", "title", "desc", "creater_id", "create_time"))
        extend_album_info(di, request.user.id)
        return JsonResponse(di)
        return render(request, 'picture/get_album_info.html', di)

    def put(self, request, album_id, *args, **kwargs):
        return JsonResponse({"code": 0, "msg": "成功", "data": "暂未开发"})

    def delete(self, request, album_id, *args, **kwargs):
        return JsonResponse({"code": 0, "msg": "成功", "data": "暂未开发"})


class AlbumAddInfoView(LoginRequiredMixin, View):
    login_url = reverse('user:user_login')

    def post(self, request, album_id, *args, **kwargs):
        return JsonResponse({"code": 0, "msg": "成功", "data": "暂未开发"})


class ReplyInfoView(LoginRequiredMixin, View):
    login_url = reverse('user:user_login')

    def get(self, request, reply_id, *args, **kwargs):
        return JsonResponse({"code": 0, "msg": "成功", "data": "暂未开发"})

    def put(self, request, reply_id, *args, **kwargs):
        return JsonResponse({"code": 0, "msg": "成功", "data": "暂未开发"})

    def delete(self, request, reply_id, *args, **kwargs):
        return JsonResponse({"code": 0, "msg": "成功", "data": "暂未开发"})


class ReplyAddInfoView(LoginRequiredMixin, View):
    login_url = reverse('user:user_login')

    def post(self, request, *args, **kwargs):
        return JsonResponse({"code": 0, "msg": "成功", "data": "暂未开发"})


class FavoriteAlbumView(LoginRequiredMixin, View):
    login_url = reverse('user:user_login')

    def get(self, request, *args, **kwargs):
        # 添加、删除收藏文章
        album_id = request.GET.get("album_id")
        obj_id = -1

        if not album_id:
            return JsonResponse({"code": 101, 'msg': '缺少 album_id'})

        if FavoriteAlbum.objects.filter(album_id=album_id, creater_id=request.user.id).count() > 0:
            FavoriteAlbum.objects.filter(album_id=album_id, creater_id=request.user.id).delete()
        else:
            obj_id = FavoriteAlbum.objects.create(album_id=album_id, creater_id=request.user.id).id
        update_favorite_album_count(album_id)

        return JsonResponse({'code': 0, 'msg': '成功', 'data': {'id': obj_id}})
