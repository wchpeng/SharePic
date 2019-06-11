from celery import shared_task

from django.core.cache import cache
from django.conf import settings

from .models import FavoriteAlbum, Reply

REPLY_ALBUM_CACHE_KEY = settings.REPLY_ALBUM_CACHE_KEY
FAVORITE_ALBUM_CACHE_KEY = settings.FAVORITE_ALBUM_CACHE_KEY


@shared_task
def celery_update_favorite_album_count(album_id):
    # 保存相册收藏数
    update_count(key="album_id", value=album_id, obj=FavoriteAlbum, cache_key_format=FAVORITE_ALBUM_CACHE_KEY)


@shared_task
def celery_update_reply_album_count(album_id):
    # 更新回复相册数
    update_count(key="album_id", value=album_id, obj=Reply, cache_key_format=REPLY_ALBUM_CACHE_KEY)


def update_count(key, value, obj, cache_key_format):
    # 保存统计数
    if not all([key, value]):
        return "no key value"
    num = obj.objects.filter(**{key: value}).count()
    cache.set(cache_key_format.format(value), num)
    return 'success'
