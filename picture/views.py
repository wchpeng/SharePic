from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import Picture, Album


class IndexView(TemplateView):

    template_name = "picture/index.html"

    def get_limit(self):
        page_size = int(self.request.GET.get("page_size", 18))
        page_no = int(self.request.GET.get("page_no", 1))
        if page_size > 50:
            page_size = 18
        return (page_no-1)*page_size, page_no*page_size

    def get_context_data(self, **kwargs):
        start, end = self.get_limit()
        albums = Album.objects.all().only("id", "create_time", "title", "desc", "creater_id").order_by("-id")[start:end]
        values = albums.values("id", "create_time", "title", "desc", "creater_id")
        album_ids = [v["id"] for v in values]
        return values