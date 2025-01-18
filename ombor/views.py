from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ViewSet
from .models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka
from .models import OlinganMaxsulot, Buyurtma, Talabnoma, RadEtilganMaxsulot
from .models import KorzinkaMaxsulot
from .serializers import JamiMahsulotGetSerializer
from .serializers import KategoriyaPostSerializer, KategoriyaGetSerializer
from .serializers import MaxsulotGetSerializer, MaxsulotPostSerializer
from .serializers import BuyurtmaSerializer
from .serializers import KorzinkaMaxsulotPostSerializer
from .serializers import KorzinkaSerializer
from .serializers import BirlikSerializer, OmborniYopishSerializer
from .serializers import OmborGetSerializer, OmborPostSerializer
from .serializers import OlinganMaxsulotSerializer, OlinganMaxsulotPostSerializer
from .serializers import TalabnomaSerializer, JamiMahsulotGetSerializer
from .serializers import RadEtilganMaxsulotSerializer, RadEtilganMaxsulotPostSerializer

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
    http_method_names = ['get', 'post', 'patch']


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
    queryset = Buyurtma.objects.filter(active=True)
    serializer_class = BuyurtmaSerializer
    http_method_names = ['get', 'patch']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['komendant_user', 'tasdiqlash', 'rad_etish']



# korzinka

class KorzinkaViewSet(ModelViewSet):
    queryset = Korzinka.objects.all()
    serializer_class = KorzinkaSerializer
    http_method_names = ['get', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['komendant_user', 'maxsulot_role']



class KorzinkaMaxsulotViewSet(ModelViewSet):
    queryset = KorzinkaMaxsulot.objects.all()
    serializer_class = KorzinkaMaxsulotPostSerializer
    http_method_names = ['post', 'delete']
    

    def perform_create(self, serializer):
        maxsulot = serializer.validated_data['maxsulot']
        qiymat = serializer.validated_data['qiymat']
        user = self.request.user

        # Mahsulot roli asosida korzinka topish yoki yaratish
        korzinka, created = Korzinka.objects.get_or_create(
            komendant_user=user,
            maxsulot_role=maxsulot.maxsulot_role,  # Mahsulot roli asosida korzinka
        )

        # Mahsulotni korzinkaga qo'shish
        if not KorzinkaMaxsulot.objects.filter(korzinka=korzinka, maxsulot=maxsulot).exists():
            # Mahsulotni yaratish
            serializer.save(korzinka=korzinka)
        else:
            raise ValidationError("Bu mahsulot allaqachon korzinkada mavjud.")

    def create(self, request, *args, **kwargs):
        """
        Create a new KorzinkaMaxsulot, only if the product is not already in the cart.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
                return Response({"message": "Mahsulot korzinkaga muvaffaqiyatli qo'shildi."}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
# olingan maxsulot

class OlinganMaxsulotViewSet(ModelViewSet):
    queryset = OlinganMaxsulot.objects.all()
    http_method_names = ['get', 'patch']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buyurtma__komendant_user']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # GET uchun
            return OlinganMaxsulotSerializer
        return OlinganMaxsulotPostSerializer  # POST, PUT, PATCH uchun



# rad etilgan maxsulot 

class RadEtilganMaxsulotlarViewSet(ModelViewSet):
    queryset = RadEtilganMaxsulot.objects.all()
    http_method_names = ['get', 'patch']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buyurtma__komendant_user']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # GET uchun
            return RadEtilganMaxsulotSerializer
        return RadEtilganMaxsulotPostSerializer  # POST, PUT, PATCH uchun



# jami maxsulot


# class JamiMahsulotViewSet(ViewSet):

#     def list(self, request):
#         """
#         Jami mahsulotlar ro'yxatini GET orqali chiqarish.
#         """
#         try:
#             queryset = Kategoriya.objects.all()
#             serializer = JamiMahsulotGetSerializer(queryset, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Kategoriya.DoesNotExist:
#             return Response({"error": " maxsulot topilmadi."}, status=status.HTTP_404_NOT_FOUND)
    

from rest_framework import viewsets, status
from rest_framework.response import Response
from decimal import Decimal
from django.db.models import Sum
from .models import BuyurtmaMaxsulot, Ombor, OlinganMaxsulot, JamiMahsulot
from .serializers import JamiMahsulotGetSerializer

class JamiMahsulotViewSet(viewsets.ViewSet):

    def list(self, request):
        """
        Barcha mahsulotlar ro'yxatini GET orqali chiqarish va hisoblash.
        """
        try:
            # Barcha JamiMahsulotlarni JSON formatida qaytarish
            queryset = Kategoriya.objects.all() # JamiMahsulotlar ro'yxati
            serializer = JamiMahsulotGetSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except BuyurtmaMaxsulot.DoesNotExist:
            return Response({"error": "Maxsulot topilmadi."}, status=status.HTTP_404_NOT_FOUND)





class TalabnomaViewSet(ModelViewSet):
    queryset = Talabnoma.objects.all()
    serializer_class = TalabnomaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buyurtma']









