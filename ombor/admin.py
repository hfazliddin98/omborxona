from django.contrib import admin
from .models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka
from .models import OlinganMaxsulotlar


@admin.register(Kategoriya)
class KategoriyaAdmin(admin.ModelAdmin):
    list_display  = ['name']

@admin.register(Maxsulot)
class MaxsulotNomiAdmin(admin.ModelAdmin):
    list_display  = ['kategoriya', 'name']

@admin.register(Birlik)
class BirlikAdmin(admin.ModelAdmin):
    list_display  = ['name']

@admin.register(OmborniYopish)
class OmborniYopishAdmin(admin.ModelAdmin):
    list_display  = ['yopish']

@admin.register(Ombor)
class OmborAdmin(admin.ModelAdmin):
    list_display  = ['maxsulot', 'qiymat', 'birlik']

@admin.register(Korzinka)
class KorzinkaNomiAdmin(admin.ModelAdmin):
    list_display  = ['user', 'maxsulot', 'qiymat', 'birlik', 'active']

@admin.register(OlinganMaxsulotlar)
class OlinganMaxsulotlarAdmin(admin.ModelAdmin):
    list_display  = ['user', 'maxsulot', 'qiymat', 'birlik', 'active']

