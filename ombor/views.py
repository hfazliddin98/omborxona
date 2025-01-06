from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka
from .models import OlinganMaxsulot, Buyurtma, Talabnoma, RadEtilganMaxsulot
from .models import KorzinkaMaxsulot, BuyurtmaMaxsulot
from .serializers import JamiMahsulotGetSerializer
from .serializers import KategoriyaPostSerializer, KategoriyaGetSerializer
from .serializers import MaxsulotGetSerializer, MaxsulotPostSerializer
from .serializers import BuyurtmaGetSerializer, BuyurtmaPostSerializer, BuyurtmaMaxsulotGetSerializer, BuyurtmaMaxsulotPostSerializer
from .serializers import KorzinkaMaxsulotGetSerializer, KorzinkaMaxsulotPostSerializer
from .serializers import KorzinkaGetSerializer, KorzinkaPostSerializer
from .serializers import BirlikSerializer, OmborniYopishSerializer
from .serializers import OmborGetSerializer, OmborPostSerializer
from .serializers import OlinganMaxsulotGetSerializer, OlinganMaxsulotPostSerializer
from .serializers import JamiMahsulotGetSerializer, TalabnomaSerializer
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


# ombor 

class OmborniYopishViewSet(ModelViewSet):
    queryset = OmborniYopish.objects.all()
    serializer_class = OmborniYopishSerializer


class OmborViewSet(ModelViewSet):
    queryset = Ombor.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['maxsulot', 'qiymat']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # GET uchun
            return OmborGetSerializer  # Maxsus serializer
        return OmborPostSerializer  # POST, PUT, PATCH uchun


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['komendant_user']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # GET uchun
            return KorzinkaGetSerializer
        return KorzinkaPostSerializer # POST, PUT, PATCH uchun

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



class KategoriyaWithJamiMahsulotView(APIView):
    """
    Kategoriya va mahsulotlar ro'yxatini GET orqali chiqarish.
    """
    def get(self, request, *args, **kwargs):
        kategoriyalar = Kategoriya.objects.all()
        serializer = JamiMahsulotGetSerializer(kategoriyalar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class TalabnomaViewSet(ModelViewSet):
    queryset = Talabnoma.objects.all()
    serializer_class = TalabnomaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buyurtma']









