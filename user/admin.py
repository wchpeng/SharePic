from django.contrib import admin

from .models import User, RelationInUser

admin.site.register(User)
admin.site.register(RelationInUser)
