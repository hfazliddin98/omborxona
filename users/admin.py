from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import Users

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display  = [
        'username',
        'first_name',
        'last_name',
        'parol',
        'superadmin',
        'omborchi',
        'komendant',
        'is_superuser'
    ]


admin.site.unregister(Group)