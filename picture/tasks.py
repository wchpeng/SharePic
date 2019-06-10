from celery import shared_task

from django.core.cache import cache


@shared_task
def update_count(key, value, obj, cache_key_format):
    # 保存统计数
    if not value:
        return
    num = obj.objects.filter(**{key: value}).count()
    cache.set(cache_key_format.format(value), num)
