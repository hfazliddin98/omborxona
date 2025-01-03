import os
import xlwt
import qrcode
import datetime as dt
from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework.decorators import action
from xhtml2pdf import pisa
from rest_framework import generics
from rest_framework import views
from rest_framework import filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka
from .models import OlinganMaxsulotlar, Buyurtma, JamiMahsulot, Talabnoma, RadEtilganMaxsulotlar
from .models import KorzinkaMaxsulot
from .serializers import KategoriyaSerializer, KorzinkaSerializer
from .serializers import BirlikSerializer, OmborniYopishSerializer, OmborSerializer
from .serializers import OlinganMaxsulotlarSerializer, BuyurtmaSearchSerializer
from .serializers import JamiMahsulotSerializer, TalabnomaSerializer, RadEtilganMaxsulotlarSerializer
from ombor import serializers
from ombor import models


class KategoriyaViewSet(ModelViewSet):
    queryset = Kategoriya.objects.all()
    serializer_class = KategoriyaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

class MaxsulotViewSet(ModelViewSet):
    queryset = Maxsulot.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['kategoriya', 'maxviylik', 'birlik']
        
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # GET uchun
            return serializers.MaxsulotGetSerializer
        return serializers.MaxsulotPostSerializer  # POST, PUT, PATCH uchun

class BirlikViewSet(ModelViewSet):
    queryset = Birlik.objects.all()
    serializer_class = BirlikSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

class OmborniYopishViewSet(ModelViewSet):
    queryset = OmborniYopish.objects.all()
    serializer_class = OmborniYopishSerializer


class OmborViewSet(ModelViewSet):
    queryset = Ombor.objects.all()
    serializer_class = OmborSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['maxsulot', 'qiymat']


# buyutma
 

class BuyurtmaViewSet(ModelViewSet):
    queryset = Buyurtma.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tasdiqlash', 'rad_etish']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # GET uchun
            return serializers.BuyurtmaGetSerializer
        return serializers.BuyurtmaPostSerializer  # POST, PUT, PATCH uchun

class BuyurtmaMaxsulotViewSet(ModelViewSet):
    queryset = models.BuyurtmaMaxsulot.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buyurtma', 'maxsulot', 'qiymat']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # GET uchun
            return serializers.BuyurtmaMaxsulotGetSerializer
        return serializers.BuyurtmaMaxsulotPostSerializer  # POST, PUT, PATCH uchun


# korzinka

class KorzinkaViewSet(ModelViewSet):
    queryset = Korzinka.objects.all()
    serializer_class = KorzinkaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['komendant_user']

    

class KorzinkaMaxsulotViewSet(ModelViewSet):
    queryset = KorzinkaMaxsulot.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['korzinka', 'maxsulot', 'qiymat', 'sorov']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # GET uchun
            return serializers.KorzinkaGetMaxsulotSerializer
        return serializers.KorzinkaPostMaxsulotSerializer  # POST, PUT, PATCH uchun

    



class OlinganMaxsulotlarViewSet(ModelViewSet):
    queryset = OlinganMaxsulotlar.objects.all()
    serializer_class = OlinganMaxsulotlarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buyurtma', 'maxsulot', 'qiymat']

class RadEtilganMaxsulotlarViewSet(ModelViewSet):
    queryset = RadEtilganMaxsulotlar.objects.all()
    serializer_class = RadEtilganMaxsulotlarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rad_etgan_user', 'buyurtma', 'maxsulot', 'qiymat']

class JamiMahsulotViewSet(ModelViewSet):
    queryset = JamiMahsulot.objects.all()
    serializer_class = JamiMahsulotSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['maxsulot', 'qiymat']

class TalabnomaViewSet(ModelViewSet):
    queryset = Talabnoma.objects.all()
    serializer_class = TalabnomaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buyurtma']




class BuyurtmaSearchView(generics.ListAPIView):
    queryset = Buyurtma.objects.all()
    serializer_class = BuyurtmaSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']




