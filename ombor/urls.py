from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import KategoriyaViewSet, MaxsulotViewSet, BirlikViewSet, OmborniYopishViewSet, OmborViewSet
from .views import KorzinkaViewSet, OlinganMaxsulotlarViewSet, BuyurtmaViewSet, BuyurtmaSearchView
from .views import JamiMahsulotViewSet, RadEtilganMaxsulotlarViewSet

from .views import TalabnomaListAPIView


router = SimpleRouter()
router.register(r'kategoriya', KategoriyaViewSet, basename='kategoriya')
router.register(r'mahsulot', MaxsulotViewSet, basename='mahsulot')
router.register(r'birlik', BirlikViewSet, basename='birlik')
router.register(r'omborni_yopish', OmborniYopishViewSet, basename='omborni_yopish')
router.register(r'ombor', OmborViewSet, basename='ombor')
router.register(r'buyurtma', BuyurtmaViewSet, basename='buyurtma')
router.register(r'korzinka', KorzinkaViewSet, basename='korzinka')
router.register(r'olingan_maxsulotlar', OlinganMaxsulotlarViewSet, basename='olingan_maxsulotlar')
router.register(r'rad_etilgan_maxsulotlar', RadEtilganMaxsulotlarViewSet, basename='rad_etilgan_maxsulotlar')
router.register(r'jami_maxsulotlar', JamiMahsulotViewSet, basename='jami_maxsulotlar')


urlpatterns = [
    path('buyurtma_search/', BuyurtmaSearchView.as_view(), name='buyurtma_search'),
    path('talabnoma/<str:pk>/', TalabnomaListAPIView.as_view(), name='talabnoma')
]
urlpatterns += router.urls
