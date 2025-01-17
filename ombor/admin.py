from django.contrib import admin
from .models import Kategoriya, Maxsulot, Birlik
from .models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka, JamiMahsulot
from .models import OlinganMaxsulot, Buyurtma, RadEtilganMaxsulot, Talabnoma, BuyurtmaMaxsulot


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
    

@admin.register(Buyurtma)
class BuyurtmaAdmin(admin.ModelAdmin):
    list_display  = ['komendant_user']

@admin.register(BuyurtmaMaxsulot)
class BuyurtmaMaxsulotAdmin(admin.ModelAdmin):
    list_display  = ['qiymat']

@admin.register(Korzinka)
class KorzinkaAdmin(admin.ModelAdmin):
    list_display  = ['komendant_user']

@admin.register(OlinganMaxsulot)
class OlinganMaxsulotAdmin(admin.ModelAdmin):
    list_display  = ['buyurtma']


