from django.contrib import admin
from .models import Kategoriya, Maxsulot, Birlik
from .models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka, JamiMahsulot
from .models import OlinganMaxsulot, Buyurtma, RadEtilganMaxsulot, Talabnoma


@admin.register(Kategoriya)
class KategoriyaAdmin(admin.ModelAdmin):
    list_display  = ['name']
    list_filter  = ['name']

@admin.register(Maxsulot)
class MaxsulotNomiAdmin(admin.ModelAdmin):
    list_display  = ['name']
    list_filter = ['name']

@admin.register(Birlik)
class BirlikAdmin(admin.ModelAdmin):
    list_display  = ['name']
    list_filter  = ['name']

@admin.register(OmborniYopish)
class OmborniYopishAdmin(admin.ModelAdmin):
    list_display  = ['yopish']

@admin.register(Ombor)
class OmborAdmin(admin.ModelAdmin):
    list_display  = ['maxsulot']

@admin.register(JamiMahsulot)
class JamiMahsulotAdmin(admin.ModelAdmin):
    list_display  = ['id', 'maxsulot', 'qiymat']
    

# @admin.register(Buyurtma)
# class BuyurtmaAdmin(admin.ModelAdmin):
#     list_display  = ['user', 'active']
#     list_filter  = ['user', 'active']

# @admin.register(Korzinka)
# class KorzinkaNomiAdmin(admin.ModelAdmin):
#     list_display  = ['buyurtma', 'maxsulot', 'qiymat', 'birlik', 'active']
#     list_filter = ['buyurtma', 'maxsulot', 'qiymat', 'birlik', 'active']

# @admin.register(OlinganMaxsulot)
# class OlinganMaxsulotlarAdmin(admin.ModelAdmin):
#     list_display  = ['buyurtma', 'maxsulot', 'qiymat', 'birlik', 'active']
#     list_filter = ['buyurtma', 'maxsulot', 'qiymat', 'birlik', 'active']

# @admin.register(RadEtilganMaxsulot)
# class RadEtilganMaxsulotlarAdmin(admin.ModelAdmin):
#     list_display  = ['buyurtma', 'maxsulot', 'qiymat', 'birlik', 'active']
#     list_filter = ['buyurtma', 'maxsulot', 'qiymat', 'birlik', 'active']

# @admin.register(Talabnoma)
# class TalabnomaAdmin(admin.ModelAdmin):
#     list_display  = ['buyurtma']
#     list_filter = ['buyurtma']

