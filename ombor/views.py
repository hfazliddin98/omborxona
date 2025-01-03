from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka
from .models import OlinganMaxsulot, Buyurtma, JamiMahsulot, Talabnoma, RadEtilganMaxsulot
from .models import KorzinkaMaxsulot, BuyurtmaMaxsulot
from .serializers import KategoriyaPostSerializer, KategoriyaGetSerializer
from .serializers import MaxsulotGetSerializer, MaxsulotPostSerializer
from .serializers import BuyurtmaGetSerializer, BuyurtmaPostSerializer, BuyurtmaMaxsulotGetSerializer, BuyurtmaMaxsulotPostSerializer
from .serializers import KorzinkaMaxsulotGetSerializer, KorzinkaMaxsulotPostSerializer
from .serializers import KorzinkaSerializer
from .serializers import BirlikSerializer, OmborniYopishSerializer, OmborSerializer
from .serializers import OlinganMaxsulotGetSerializer, OlinganMaxsulotPostSerializer
from .serializers import JamiMahsulotSerializer, TalabnomaSerializer
from .serializers import RadEtilganMaxsulotGetSerializer, RadEtilganMaxsulotPostSerializer

class KategoriyaViewSet(ModelViewSet):
    queryset = Kategoriya.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

      
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # GET uchun
            return KategoriyaGetSerializer
        return KategoriyaPostSerializer  # POST, PUT, PATCH uchun

class MaxsulotViewSet(ModelViewSet):
    queryset = Maxsulot.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['kategoriya', 'maxviylik', 'birlik']
        
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # GET uchun
            return MaxsulotGetSerializer
        return MaxsulotPostSerializer  # POST, PUT, PATCH uchun

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
            return BuyurtmaGetSerializer
        return BuyurtmaPostSerializer  # POST, PUT, PATCH uchun

class BuyurtmaMaxsulotViewSet(ModelViewSet):
    queryset = BuyurtmaMaxsulot.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buyurtma', 'maxsulot', 'qiymat']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # GET uchun
            return BuyurtmaMaxsulotGetSerializer
        return BuyurtmaMaxsulotPostSerializer  # POST, PUT, PATCH uchun


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
            return KorzinkaMaxsulotGetSerializer
        return KorzinkaMaxsulotPostSerializer # POST, PUT, PATCH uchun

    
# olingan maxsulot

class OlinganMaxsulotViewSet(ModelViewSet):
    queryset = OlinganMaxsulot.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buyurtma', 'maxsulot', 'qiymat']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # GET uchun
            return OlinganMaxsulotGetSerializer
        return OlinganMaxsulotPostSerializer  # POST, PUT, PATCH uchun


# rad etilgan maxsulot 

class RadEtilganMaxsulotlarViewSet(ModelViewSet):
    queryset = RadEtilganMaxsulot.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rad_etgan_user', 'buyurtma', 'maxsulot', 'qiymat']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # GET uchun
            return RadEtilganMaxsulotGetSerializer
        return RadEtilganMaxsulotPostSerializer  # POST, PUT, PATCH uchun


# jami maxsulot

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









