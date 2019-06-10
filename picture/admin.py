from django.contrib import admin

from .models import Picture, Album, AlbumCategory, AlbumTag, Reply, FavoriteAlbum
from SharePic.admin import MyselfInfoList


class AlbumAdmin(MyselfInfoList):
    filter_horizontal = ["tags"]


admin.site.register(Picture, MyselfInfoList)
admin.site.register(Album, AlbumAdmin)
admin.site.register(AlbumTag, MyselfInfoList)
admin.site.register(AlbumCategory, MyselfInfoList)
admin.site.register(FavoriteAlbum, MyselfInfoList)
admin.site.register(Reply, MyselfInfoList)
