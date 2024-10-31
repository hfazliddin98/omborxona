from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Kategoriya, MaxsulotNomi, Birlik, OmborniYopish, Ombor
from .serializers import KategoriyaSerializer, MaxsulotNomiSerializer
from .serializers import BirlikSerializer, OmborniYopishSerializer, OmborSerializer



class KategoriyaViewSet(ModelViewSet):
    queryset = Kategoriya.objects.all()
    serializer_class = KategoriyaSerializer

class MaxsulotNomiViewSet(ModelViewSet):
    queryset = MaxsulotNomi.objects.all()
    serializer_class = MaxsulotNomiSerializer

class BirlikViewSet(ModelViewSet):
    queryset = Birlik.objects.all()
    serializer_class = BirlikSerializer

class OmborniYopishViewSet(ModelViewSet):
    queryset = OmborniYopish.objects.all()
    serializer_class = OmborniYopishSerializer

class OmborViewSet(ModelViewSet):
    queryset = Ombor.objects.all()
    serializer_class = OmborSerializer
