from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # 用户表，可扩展字段
    pass


class RelationInUser(models.Model):
    """
    用户关系表：
        关系有：关注，朋友
    """
    USER_RELATION_CHOICE = (
        (1, "关注"),  # 关注表示 from_user 关注 to_user, to_user 没有关注 from_user
        (2, "朋友")  # 朋友表示双方相互关注
    )
    from_user = models.IntegerField(verbose_name="关注者")
    to_user = models.IntegerField(verbose_name="被关注者")
    relation = models.PositiveSmallIntegerField(choices=USER_RELATION_CHOICE, verbose_name="双方关系")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return "%d - %d - %s" % (self.from_user, self.to_user, self.get_relation_display())

    class Meta:
        verbose_name = "用户关系"
        verbose_name_plural = "用户关系"
