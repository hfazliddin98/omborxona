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
from .serializers import KategoriyaSerializer, MaxsulotSerializer, KorzinkaSerializer
from .serializers import BirlikSerializer, OmborniYopishSerializer, OmborSerializer
from .serializers import OlinganMaxsulotlarSerializer, BuyurtmaSerializer, BuyurtmaSearchSerializer
from .serializers import JamiMahsulotSerializer, TalabnomaSerializer, RadEtilganMaxsulotlarSerializer, BuyurtmaListSerializer


class KategoriyaViewSet(ModelViewSet):
    queryset = Kategoriya.objects.all()
    serializer_class = KategoriyaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

class MaxsulotViewSet(ModelViewSet):
    queryset = Maxsulot.objects.all()
    serializer_class = MaxsulotSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['kategoriya', 'name', 'maxviylik', 'it_park']

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
    filterset_fields = ['maxsulot', 'qiymat', 'birlik']


class BuyurtmaViewSet(ModelViewSet):
    queryset = Buyurtma.objects.all()
    serializer_class = BuyurtmaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buyurtma']
    filterset_fields = ['user', 'active', 'sorov', 'rad']

    def get_serializer_class(self):
        if self.action == 'list':
            return BuyurtmaListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        role = self.request.user.role
        qs = super().get_queryset()
        if self.action == "list":
            qs = qs.filter(role=role).prefetch_related(
                "korzinka_set"
            )
        return qs

class KorzinkaViewSet(ModelViewSet):
    queryset = Korzinka.objects.all()
    serializer_class = KorzinkaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buyurtma', 'maxsulot', 'qiymat', 'birlik', 'active']

class OlinganMaxsulotlarViewSet(ModelViewSet):
    queryset = OlinganMaxsulotlar.objects.all()
    serializer_class = OlinganMaxsulotlarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buyurtma', 'maxsulot', 'qiymat', 'birlik', 'active']

class RadEtilganMaxsulotlarViewSet(ModelViewSet):
    queryset = RadEtilganMaxsulotlar.objects.all()
    serializer_class = RadEtilganMaxsulotlarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'buyurtma', 'maxsulot', 'qiymat', 'birlik', 'active']

class JamiMahsulotViewSet(ModelViewSet):
    queryset = JamiMahsulot.objects.all()
    serializer_class = JamiMahsulotSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['maxsulot', 'qiymat', 'birlik']

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




