from django.core.cache import cache
from django.conf import settings

from user.models import User
from .models import FavoriteAlbum, Reply, Picture
from .tasks import update_count, celery_update_favorite_album_count, celery_update_reply_album_count

REPLY_ALBUM_CACHE_KEY = settings.REPLY_ALBUM_CACHE_KEY
FAVORITE_ALBUM_CACHE_KEY = settings.FAVORITE_ALBUM_CACHE_KEY


def extend_count(data, uid):
    # 为 data 中扩展收藏数（favorite_count）和回复数（reply_count）和用户名（user_username）

    # 扩展 album 创建者用户名
    user_ids = list(set([d["creater_id"] for d in data]))
    usernames = User.objects.filter(id__in=user_ids).values("id", "username")
    user_id_name_map = {u["id"]: u["username"] for u in usernames}

    # 扩展 album 第一张图片 url
    first_picture_ids = list(set([d["first_picture_id"] for d in data]))
    picture_urls = Picture.objects.filter(id__in=first_picture_ids).only("id", "picture")
    picture_id_map = {p.id: p.picture.url for p in picture_urls}

    # 扩展我是否对 album 关注
    if uid:
        album_ids = [i['id'] for i in data]
        favorite_albums = FavoriteAlbum.objects.filter(creater_id=uid, album_id__in=album_ids).values('album_id')
        favorite_album_ids = set([i['album_id'] for i in favorite_albums])
    else:
        favorite_album_ids = set()

    for d in data:
        d["user__username"] = user_id_name_map.get(d.get("creater_id"), "")
        d["first_picture"] = picture_id_map.get(d.get("first_picture_id"), "/static/base/bg_groups/green.jpg")

        if "id" not in d:
            d["reply_count"] = 0
            d["favorite_count"] = 0
            continue
        album_id = d["id"]
        d["reply_count"] = get_reply_album_count(album_id)
        d["favorite_count"] = get_favorite_album_count(album_id)
        d["is_favorite"] = album_id in favorite_album_ids


def get_favorite_album_count(album_id):
    # 获取相册收藏数
    return get_count(key="album_id", value=album_id, obj=FavoriteAlbum, cache_key_format=FAVORITE_ALBUM_CACHE_KEY)


def update_favorite_album_count(album_id):
    # 保存相册收藏数
    celery_update_favorite_album_count.delay(album_id)


def get_reply_album_count(album_id):
    # 回复相册数
    return get_count(key="album_id", value=album_id, obj=Reply, cache_key_format=REPLY_ALBUM_CACHE_KEY)


def update_reply_album_count(album_id):
    # 更新回复相册数
    celery_update_reply_album_count.delay(album_id)


def get_count(key, value, obj, cache_key_format):
    # 获取统计数
    if not value:
        return 0
    num = cache.get(cache_key_format.format(value))
    if num is None:
        update_count(key, value, obj, cache_key_format)
        return cache.get(cache_key_format.format(value))
    return num
