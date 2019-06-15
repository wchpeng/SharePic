# from django.contrib import admin

from .models import User, RelationInUser
from SharePic.admin import admin

admin.site.register(User)
admin.site.register(RelationInUser)
