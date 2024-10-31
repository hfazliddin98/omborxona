from django.contrib import admin
from ombor.models import Kategoriya, MaxsulotNomi


@admin.register(Kategoriya)
class KategoriyaAdmin(admin.ModelAdmin):
    list_display  = ['name']

@admin.register(MaxsulotNomi)
class MaxsulotNomiAdmin(admin.ModelAdmin):
    list_display  = ['kategoriya', 'name']