from django.contrib import admin

from .models import Picture, Album, AlbumCategory, AlbumTag, Reply


admin.site.register(Picture)
admin.site.register(Album)
admin.site.register(AlbumTag)
admin.site.register(AlbumCategory)
admin.site.register(Reply)
