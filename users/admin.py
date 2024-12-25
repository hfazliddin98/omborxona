from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import Users, Binos

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display  = [
        'username', 'first_name', 'last_name',
        'is_superuser', 'is_active'
    ]


@admin.register(Binos)
class BinosAdmin(admin.ModelAdmin):
    list_display  = [
        'name', 
    ]
    

admin.site.unregister(Group)