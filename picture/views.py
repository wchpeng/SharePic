from django.views.generic.base import TemplateView
from django.core.paginator import Paginator
from django.db.models.query_utils import Q

from .models import Picture, Album
from .utils import extend_count


class IndexView(TemplateView):

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
        extend_count(values)  # 扩展收藏数、回复数、用户名、第一张图片

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
