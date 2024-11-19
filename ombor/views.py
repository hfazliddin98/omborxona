from django.shortcuts import render
from django.db.models import Sum 
from rest_framework import filters
from decimal import Decimal
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka
from .models import OlinganMaxsulotlar, Buyurtma, JamiMahsulot
from .serializers import KategoriyaSerializer, MaxsulotSerializer, KorzinkaSerializer
from .serializers import BirlikSerializer, OmborniYopishSerializer, OmborSerializer
from .serializers import OlinganMaxsulotlarSerializer, BuyurtmaSerializer, BuyurtmaSearchSerializer
from .serializers import JamiMahsulotSerializer


class KategoriyaViewSet(ModelViewSet):
    queryset = Kategoriya.objects.all()
    serializer_class = KategoriyaSerializer

class MaxsulotViewSet(ModelViewSet):
    queryset = Maxsulot.objects.all()
    serializer_class = MaxsulotSerializer

class BirlikViewSet(ModelViewSet):
    queryset = Birlik.objects.all()
    serializer_class = BirlikSerializer

class OmborniYopishViewSet(ModelViewSet):
    queryset = OmborniYopish.objects.all()
    serializer_class = OmborniYopishSerializer

class OmborViewSet(ModelViewSet):
    queryset = Ombor.objects.all()
    serializer_class = OmborSerializer

    def perform_create(self, serializer):
        # Ombor yozuvini saqlaydi
        instance = serializer.save()

        # JamiMahsulot jadvalidagi qiymatni yangilaydi yoki yangi yozuv yaratadi
        jami_mahsulot, created = JamiMahsulot.objects.get_or_create(
            maxsulot=instance.maxsulot,
            defaults={'qiymat': 0.0, 'birlik': instance.birlik}
        )

        # Olingan mahsulotlarning umumiy qiymatini hisoblaymiz
        olingan_jami_qiymat = OlinganMaxsulotlar.objects.filter(
            maxsulot=instance.maxsulot,
            active=True
        ).aggregate(total_qiymat=Sum('qiymat'))['total_qiymat'] or 0.0

        print(f"Joriy jami qiymat: {jami_mahsulot.qiymat}")
        print(f"Ombor qiymati: {instance.qiymat}")
        print(f"Olingan jami qiymat: {olingan_jami_qiymat}")

        # Jami mahsulot qiymatidan olingan mahsulot qiymatini ayiramiz
        jami_mahsulot.qiymat = Decimal(jami_mahsulot.qiymat) - Decimal(olingan_jami_qiymat)
        
        jami_mahsulot.save()


class BuyurtmaViewSet(ModelViewSet):
    queryset = Buyurtma.objects.all()
    serializer_class = BuyurtmaSerializer

class KorzinkaViewSet(ModelViewSet):
    queryset = Korzinka.objects.all()
    serializer_class = KorzinkaSerializer

class OlinganMaxsulotlarViewSet(ModelViewSet):
    queryset = OlinganMaxsulotlar.objects.all()
    serializer_class = OlinganMaxsulotlarSerializer

class JamiMahsulotViewSet(ModelViewSet):
    queryset = JamiMahsulot.objects.all()
    serializer_class = JamiMahsulotSerializer



class BuyurtmaSearchView(ListAPIView):
    queryset = Buyurtma.objects.all()
    serializer_class = BuyurtmaSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']
