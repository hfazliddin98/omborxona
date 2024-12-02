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



class BuyurtmaSearchView(generics.ListAPIView):
    queryset = Buyurtma.objects.all()
    serializer_class = BuyurtmaSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']


class TalabnomaListAPIView(views.APIView):

    # def pdf_create(request, pk):
    #     template_path = 'talaba/shartnoma.html' 
    #     hozir = dt.datetime.now()

    #     context = {
    #         'shartnomalar':shartnomalar,
    #         'hozir':hozir,
    #     }
    #     response = HttpResponse(content_type='application/pdf')
    #     response['Content-Disposition'] = 'filename="shartnoma.pdf"'
    #     #   


    #     template = get_template(template_path)
    #     html = template.render(context)

    #     pisa_status = pisa.CreatePDF(html, dest=response)

    #     if pisa_status.err:
    #         return HttpResponse("Bizda ba'zi xatolar bor edi " + html + " serverda texnik ish lar olib borilmoqda !!!")
    #     return response


    def get(self, request, pk, format=False):
        buyurtma = Buyurtma.objects.get(id=pk)
        if buyurtma.prorektor==True and buyurtma.bugalter==True and buyurtma.omborchi==True and (buyurtma.it_park==True or buyurtma.xojalik_bolimi):

        
            return Response(buyurtma.id)
        else:
            return Response('xato')
