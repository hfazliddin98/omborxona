from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.response import Response
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
from .serializers import OlinganMaxsulotSerializer
from .serializers import TalabnomaSerializer, JamiMahsulotGetSerializer
from .serializers import RadEtilganMaxsulotSerializer

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
    filterset_fields = ['tasdiqlash', 'rad_etish']



# korzinka


class KorzinkaViewSet(ViewSet):

    def list(self, request):
        try:
            # queryset = Korzinka.objects.filter(komendant_user=request.user)
            queryset = Korzinka.objects.all()
            serializer = KorzinkaSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Korzinka.DoesNotExist:
            return Response({"error": "Korzinka topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            queryset = Korzinka.objects.get(pk=pk, komendant_user=request.user)
            queryset.delete()  # This actually deletes the object
            return Response({"message": "Korzinka o`chirildi."}, status=status.HTTP_204_NO_CONTENT)  # HTTP 204 for successful deletion
        except Korzinka.DoesNotExist:
            return Response({"error": "Korzinka topilmadi."}, status=status.HTTP_404_NOT_FOUND)  # Handle the case if not found


class KorzinkaMaxsulotViewSet(ViewSet):
    def create(self, request):
        # Serializer bilan validatsiya
        serializer = KorzinkaMaxsulotPostSerializer(data=request.data)
        
        if serializer.is_valid():
            maxsulot = serializer.validated_data['maxsulot']
            qiymat = serializer.validated_data['qiymat']
            user = request.user

            # Mahsulot roliga mos korzinkani topish yoki yaratish
            korzinka, created = Korzinka.objects.get_or_create(
                komendant_user=user,
                maxsulot_role=maxsulot.maxsulot_role,  # Mahsulot roli asosida korzinka
            )

            # Mahsulotni korzinkaga qo'shish
            if not KorzinkaMaxsulot.objects.filter(korzinka=korzinka, maxsulot=maxsulot).exists():
                KorzinkaMaxsulot.objects.create(
                    korzinka=korzinka,
                    maxsulot=maxsulot,
                    qiymat=qiymat,
                )
                return Response(
                    {"message": "Mahsulot korzinkaga muvaffaqiyatli qo'shildi."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"error": "Bu mahsulot allaqachon korzinkada mavjud."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, pk=None):
        try:
            queryset = KorzinkaMaxsulot.objects.get(pk=pk)
            queryset.delete()  # This actually deletes the object
            return Response({"message": "KorzinkaMaxsulot o`chirildi."}, status=status.HTTP_204_NO_CONTENT)  # HTTP 204 for successful deletion
        except KorzinkaMaxsulot.DoesNotExist:
            return Response({"error": "KorzinkaMaxsulot topilmadi."}, status=status.HTTP_404_NOT_FOUND)  # Handle the case if not found


    
# olingan maxsulot

class OlinganMaxsulotViewSet(ModelViewSet):
    queryset = OlinganMaxsulot.objects.all()
    serializer_class = OlinganMaxsulotSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buyurtma']



# rad etilgan maxsulot 

class RadEtilganMaxsulotlarViewSet(ModelViewSet):
    queryset = RadEtilganMaxsulot.objects.all()
    serializer_class = RadEtilganMaxsulotSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rad_etgan_user', 'buyurtma']



# jami maxsulot


class JamiMahsulotViewSet(ViewSet):

    def list(self, request):
        """
        Jami mahsulotlar ro'yxatini GET orqali chiqarish.
        """
        try:
            queryset = Kategoriya.objects.all()
            serializer = JamiMahsulotGetSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Kategoriya.DoesNotExist:
            return Response({"error": " maxsulot topilmadi."}, status=status.HTTP_404_NOT_FOUND)
    




class TalabnomaViewSet(ModelViewSet):
    queryset = Talabnoma.objects.all()
    serializer_class = TalabnomaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buyurtma']









