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
from rest_framework.viewsets import ModelViewSet
from .models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka
from .models import OlinganMaxsulotlar, Buyurtma, JamiMahsulot, Talabnoma, RadEtilganMaxsulotlar
from .serializers import KategoriyaSerializer, MaxsulotSerializer, KorzinkaSerializer
from .serializers import BirlikSerializer, OmborniYopishSerializer, OmborSerializer
from .serializers import OlinganMaxsulotlarSerializer, BuyurtmaSerializer, BuyurtmaSearchSerializer
from .serializers import JamiMahsulotSerializer, TalabnomaSerializer, RadEtilganMaxsulotlarSerializer


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


class BuyurtmaViewSet(ModelViewSet):
    queryset = Buyurtma.objects.all()
    serializer_class = BuyurtmaSerializer

class KorzinkaViewSet(ModelViewSet):
    queryset = Korzinka.objects.all()
    serializer_class = KorzinkaSerializer

class OlinganMaxsulotlarViewSet(ModelViewSet):
    queryset = OlinganMaxsulotlar.objects.all()
    serializer_class = OlinganMaxsulotlarSerializer

class RadEtilganMaxsulotlarViewSet(ModelViewSet):
    queryset = RadEtilganMaxsulotlar.objects.all()
    serializer_class = RadEtilganMaxsulotlarSerializer

class JamiMahsulotViewSet(ModelViewSet):
    queryset = JamiMahsulot.objects.all()
    serializer_class = JamiMahsulotSerializer

class TalabnomaViewSet(ModelViewSet):
    queryset = Talabnoma.objects.all()
    serializer_class = TalabnomaSerializer




class BuyurtmaSearchView(generics.ListAPIView):
    queryset = Buyurtma.objects.all()
    serializer_class = BuyurtmaSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']




