from django.contrib import admin
from django.contrib.auth.models import Group

from .models import ProxyGroups
from .models import User


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Group)
admin.site.register(ProxyGroups)
admin.site.register(User, UserAdmin)
