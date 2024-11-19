from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.db.models import Sum 
from rest_framework import filters
from decimal import Decimal
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka
from .models import OlinganMaxsulotlar, Buyurtma, JamiMahsulot
from .serializers import KategoriyaSerializer, MaxsulotSerializer, KorzinkaSerializer
from .serializers import BirlikSerializer, OmborniYopishSerializer, OmborSerializer
from .serializers import OlinganMaxsulotlarSerializer, BuyurtmaSerializer, BuyurtmaSearchSerializer
from .serializers import JamiMahsulotSerializer


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

# class JamiMahsulotViewSet(ModelViewSet):
#     queryset = JamiMahsulot.objects.all()
#     serializer_class = JamiMahsulotSerializer

class JamiMahsulotListAPIView(ListAPIView):
    queryset = JamiMahsulot.objects.all()
    serializer_class = JamiMahsulotSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response_data = []

        for jami_mahsulot in queryset:
            # Olingan mahsulotlarning umumiy qiymatini hisoblash
            olingan_jami_qiymat = OlinganMaxsulotlar.objects.filter(
                maxsulot=jami_mahsulot.maxsulot,
                active=True
            ).aggregate(total_qiymat=Sum('qiymat'))['total_qiymat'] or 0.0

            # Javob ma'lumotlarini tayyorlash
            response_data.append({
                'jami_mahsulot': JamiMahsulotSerializer(jami_mahsulot).data
            })

        return Response(response_data)



class BuyurtmaSearchView(ListAPIView):
    queryset = Buyurtma.objects.all()
    serializer_class = BuyurtmaSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']
