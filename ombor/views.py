from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka
from .models import OlinganMaxsulotlar
from .serializers import KategoriyaSerializer, MaxsulotSerializer, KorzinkaSerializer
from .serializers import BirlikSerializer, OmborniYopishSerializer, OmborSerializer
from .serializers import OlinganMaxsulotlarSerializer



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

class KorzinkaViewSet(ModelViewSet):
    queryset = Korzinka.objects.all()
    serializer_class = KorzinkaSerializer

class OlinganMaxsulotlarViewSet(ModelViewSet):
    queryset = OlinganMaxsulotlar.objects.all()
    serializer_class = OlinganMaxsulotlarSerializer
