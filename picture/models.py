from django.db import models


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
    tags = models.ManyToManyField('AlbumTag', verbose_name="标签", null=True)
    first_picture_id = models.IntegerField(verbose_name="第一张图片 id", default=0)
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "相册"
        verbose_name_plural = "相册"


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
