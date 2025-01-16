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
from .models import KorzinkaMaxsulot, BuyurtmaMaxsulot
from .serializers import JamiMahsulotGetSerializer
from .serializers import KategoriyaPostSerializer, KategoriyaGetSerializer
from .serializers import MaxsulotGetSerializer, MaxsulotPostSerializer
from .serializers import BuyurtmaGetSerializer, BuyurtmaPostSerializer, BuyurtmaMaxsulotGetSerializer, BuyurtmaMaxsulotPostSerializer
from .serializers import KorzinkaMaxsulotPostSerializer
from .serializers import KorzinkaSerializer, KorzinkaMaxsulotSerializer
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

    # Ruxsat berilgan HTTP metodlari
    # http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # GET uchun
            return BuyurtmaMaxsulotGetSerializer
        return BuyurtmaMaxsulotPostSerializer  # POST, PUT, PATCH uchun


# korzinka


class KorzinkaViewSet(ViewSet):

    def list(self, request):
        try:
            queryset = Korzinka.objects.get(komendant_user=request.user)
            serializer = KorzinkaSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Korzinka.DoesNotExist:
            return Response({"error": "Korzinka topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            queryset = Korzinka.objects.get(pk=pk)
            queryset.delete()  # This actually deletes the object
            return Response({"message": "Korzinka o`chirildi."}, status=status.HTTP_204_NO_CONTENT)  # HTTP 204 for successful deletion
        except Korzinka.DoesNotExist:
            return Response({"error": "Korzinka topilmadi."}, status=status.HTTP_404_NOT_FOUND)  # Handle the case if not found

class KorzinkaMaxsulotViewSet(ViewSet):

    def create(self, request):
        # Foydalanuvchining korzinkasini olish yoki yaratish
        korzinka, created = Korzinka.objects.get_or_create(komendant_user=request.user)

        # Serializer bilan validatsiya
        serializer = KorzinkaMaxsulotPostSerializer(data=request.data)
        
        # Agar serializer to'g'ri bo'lsa, mahsulotni korzinkaga qo'shamiz
        if serializer.is_valid():
            # Maxsulot mavjudligini tekshirish
            maxsulot = serializer.validated_data['maxsulot']
            if KorzinkaMaxsulot.objects.filter(korzinka=korzinka, maxsulot=maxsulot).exists():
                return Response({"error": "Ushbu mahsulot allaqachon sizning korzinkangizda mavjud."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Mahsulotni korzinkaga qo'shish
            KorzinkaMaxsulot.objects.create(
                korzinka=korzinka,
                maxsulot=maxsulot,
                qiymat=serializer.validated_data['qiymat'],
            )
            
            # Yaratilgan yoki mavjud bo'lgan korzinkaga mahsulot qo'shildi degan xabar
            message = "Korzinka yaratildi va mahsulot muvaffaqiyatli qo'shildi." if created else "Mahsulot muvaffaqiyatli qo'shildi."
            return Response({"message": message}, status=status.HTTP_201_CREATED)
        
        # Agar serializerda xatolik bo'lsa, 400 (Bad Request) javobini qaytarish
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, pk=None):
        try:
            queryset = KorzinkaMaxsulot.objects.get(pk=pk)
            queryset.delete()  # This actually deletes the object
            return Response({"message": "KorzinkaMaxsulot o`chirildi."}, status=status.HTTP_204_NO_CONTENT)  # HTTP 204 for successful deletion
        except KorzinkaMaxsulot.DoesNotExist:
            return Response({"error": "KorzinkaMaxsulot topilmadi."}, status=status.HTTP_404_NOT_FOUND)  # Handle the case if not found


class KorzinkaAPIView(APIView):

    def get(self, request):
        try:
            korzinka = Korzinka.objects.get(komendant_user=request.user)
            serializer = KorzinkaSerializer(korzinka)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Korzinka.DoesNotExist:
            return Response({"error": "Korzinka topilmadi."}, status=status.HTTP_404_NOT_FOUND)

class KorzinkaDestroyAPIView(DestroyAPIView):
    queryset = Korzinka.objects.all()
    serializer_class = KorzinkaSerializer
    
class KorzinkaMaxsulotAPIView(APIView):

    def post(self, request):
        # Foydalanuvchining korzinkasini olish yoki yaratish
        korzinka, created = Korzinka.objects.get_or_create(komendant_user=request.user)

        # Serializer bilan validatsiya
        serializer = KorzinkaMaxsulotPostSerializer(data=request.data)
        if serializer.is_valid():
            # Mahsulotni korzinkaga qo'shish
            KorzinkaMaxsulot.objects.create(
                korzinka=korzinka,
                maxsulot=serializer.validated_data['maxsulot'],
                qiymat=serializer.validated_data['qiymat'],
            )
            message = "Korzinka yaratildi va mahsulot muvaffaqiyatli qo'shildi." if created else "Mahsulot muvaffaqiyatli qo'shildi."
            return Response({"message": message}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KorzinkaMaxsulotDestroyAPIView(DestroyAPIView):
    queryset = KorzinkaMaxsulot.objects.all()
    serializer_class = KorzinkaMaxsulotSerializer


    
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









