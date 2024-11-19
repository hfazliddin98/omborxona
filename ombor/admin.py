from django.contrib import admin
from .models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka, JamiMahsulot
from .models import OlinganMaxsulotlar, Buyurtma


@admin.register(Kategoriya)
class KategoriyaAdmin(admin.ModelAdmin):
    list_display  = ['name']
    list_filter  = ['name']

@admin.register(Maxsulot)
class MaxsulotNomiAdmin(admin.ModelAdmin):
    list_display  = ['kategoriya', 'name']
    list_filter = ['id', 'kategoriya', 'name']

@admin.register(Birlik)
class BirlikAdmin(admin.ModelAdmin):
    list_display  = ['name']
    list_filter  = ['name']

@admin.register(OmborniYopish)
class OmborniYopishAdmin(admin.ModelAdmin):
    list_display  = ['yopish']

@admin.register(Ombor)
class OmborAdmin(admin.ModelAdmin):
    list_display  = ['maxsulot', 'qiymat', 'birlik']
    list_filter  = ['maxsulot', 'qiymat', 'birlik']

@admin.register(JamiMahsulot)
class JamiMahsulotAdmin(admin.ModelAdmin):
    list_display  = ['id', 'maxsulot', 'qiymat', 'birlik']
    list_filter = ['maxsulot', 'qiymat', 'birlik']
    

@admin.register(Buyurtma)
class BuyurtmaAdmin(admin.ModelAdmin):
    list_display  = ['user', 'active']
    list_filter  = ['user', 'active']

@admin.register(Korzinka)
class KorzinkaNomiAdmin(admin.ModelAdmin):
    list_display  = ['buyurtma', 'maxsulot', 'qiymat', 'birlik', 'active']
    list_filter = ['buyurtma', 'maxsulot', 'qiymat', 'birlik', 'active']

@admin.register(OlinganMaxsulotlar)
class OlinganMaxsulotlarAdmin(admin.ModelAdmin):
    list_display  = ['buyurtma', 'maxsulot', 'qiymat', 'birlik', 'active']
    list_filter = ['buyurtma', 'maxsulot', 'qiymat', 'birlik', 'active']

