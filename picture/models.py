from itertools import chain
from collections import defaultdict, OrderedDict

from django.db import models
from django.core.cache import cache
from django.conf import settings

from user.models import User
from SharePic.utils import cache_value


class Picture(models.Model):
    """一张张的图片"""
    picture = models.ImageField(verbose_name="图片")
    desc = models.CharField(max_length=64, verbose_name="描述")
    album_id = models.IntegerField(verbose_name="相册 id")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.desc[:10] + "... - %d" % self.id

    class Meta:
        verbose_name = "图片"
        verbose_name_plural = "图片"


class Album(models.Model):
    """相册，他可以关联多张图片"""
    creater_id = models.IntegerField(verbose_name="创建者id", default=0)
    title = models.CharField(max_length=16, verbose_name="相册标题", default="")
    desc = models.CharField(max_length=64, verbose_name="相册描述", default="")
    category = models.IntegerField(verbose_name="种类", default=0)
    tags = models.ManyToManyField('AlbumTag', verbose_name="标签", blank=True)
    first_picture_id = models.IntegerField(verbose_name="第一张图片 id", default=0)
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "相册"
        verbose_name_plural = "相册"

    def to_dict(self, fields=None, exclude=None, ext=True):
        opts = self._meta
        data = {}

        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            data[f.name] = f.value_from_object(self)

        if ext:
            data["reviews"] = self.get_reviews()
            data["pictures"] = self.get_pictures()

        return data

    # @cache_value(settings.ALBUM_REVIEWS_CACHE_KEY, "id")
    def get_reviews(self):
        return get_albums_reviews_info(self.id)

    def get_pictures(self):
        data = Picture.objects.filter(album_id=self.id).only("picture")
        return [{"picture": i.picture.url} for i in data]


class AlbumCategory(models.Model):
    """相册分类"""
    name = models.CharField(max_length=16, verbose_name="分类名", default="")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return "%d - %s" % (self.id, self.name)

    class Meta:
        verbose_name = "相册分类"
        verbose_name_plural = "相册分类"


class AlbumTag(models.Model):
    """相册标签"""
    name = models.CharField(max_length=16, verbose_name="标签名", default="")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return "%d - %s" % (self.id, self.name)

    class Meta:
        verbose_name = "相册标签"
        verbose_name_plural = "相册标签"


class Reply(models.Model):
    """回复相册或图片"""
    creater_id = models.IntegerField(verbose_name="创建者", default=0)
    album_id = models.IntegerField(verbose_name="相册id", default=0)
    picture_id = models.IntegerField(verbose_name="图片id", default=0)
    parent_reply = models.IntegerField(verbose_name="回复的回复id")
    content = models.CharField(max_length=128, verbose_name="内容", default="")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return "%d - %s..." % (self.creater_id, self.content[:10])

    class Meta:
        verbose_name = "图片回复"
        verbose_name_plural = "图片回复"


class FavoriteAlbum(models.Model):
    album_id = models.IntegerField(verbose_name="相册id", default=0)
    creater_id = models.IntegerField(verbose_name="点赞人id", default=0)
    creater_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return "%d - %d" % (self.album_id, self.creater_id)

    class Meta:
        verbose_name = "点赞"
        verbose_name_plural = "点赞"


def get_field_info_id_map(kclass, ids, field):
    usernames = kclass.objects.filter(id__in=ids).values("id", field)
    return {u["id"]: u[field] for u in usernames}


def get_creater_username_and_picture(ids):
    users = User.objects.filter(id__in=ids).values("id", "username", "")


def get_albums_reviews_info(album_id):
    # 传入相册id，获取相册的回复信息
    replies = (
        Reply.objects.filter(album_id=album_id)
        .order_by("-id")
        .values(
            "id", "album_id", "parent_reply", "content", "creater_id", "create_time"
        )
    )
    creater_ids = list(set([rep["creater_id"] for rep in replies]))
    user_id_name_map = get_field_info_id_map(User, creater_ids, "username")

    first_replies = OrderedDict()
    second_replies = defaultdict(list)
    for rep in replies:
        rep["creater_username"] = user_id_name_map.get(rep["creater_id"], "")
        if rep["parent_reply"] == 0:
            first_replies[rep["id"]] = rep
        else:
            second_replies[rep["parent_reply"]].append(rep)

    for k in first_replies:
        first_replies[k]["replies"] = second_replies.get(k, [])

    return list(first_replies.values())