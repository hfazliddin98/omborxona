from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import BuyurtmaMaxsulotViewSet
from .views import KategoriyaViewSet, MaxsulotViewSet, BirlikViewSet, OmborniYopishViewSet, OmborViewSet
from .views import OlinganMaxsulotViewSet, BuyurtmaViewSet
from .views import KategoriyaWithJamiMahsulotView, RadEtilganMaxsulotlarViewSet, TalabnomaViewSet
from .views import KorzinkaAPIView, KorzinkaMaxsulotAPIView


router = SimpleRouter()
router.register(r'kategoriya', KategoriyaViewSet, basename='kategoriya')
router.register(r'maxsulot', MaxsulotViewSet, basename='maxsulot')
router.register(r'birlik', BirlikViewSet, basename='birlik')
router.register(r'omborni_yopish', OmborniYopishViewSet, basename='omborni_yopish')
router.register(r'ombor', OmborViewSet, basename='ombor')
router.register(r'buyurtma', BuyurtmaViewSet, basename='buyurtma')
router.register(r'buyurtma_maxsulot', BuyurtmaMaxsulotViewSet, basename='buyurtma_maxsulot')
router.register(r'olingan_maxsulotlar', OlinganMaxsulotViewSet, basename='olingan_maxsulotlar')
router.register(r'rad_etilgan_maxsulotlar', RadEtilganMaxsulotlarViewSet, basename='rad_etilgan_maxsulotlar')
router.register(r'talabnoma', TalabnomaViewSet, basename='talabnoma')


urlpatterns = [
    path('jami_maxsulotlar/', KategoriyaWithJamiMahsulotView.as_view(), name='jami_maxsulotlar'),
    path('korzinka/', KorzinkaAPIView.as_view(), name='korzinka'),
    path('korzinka_maxsulot/', KorzinkaMaxsulotAPIView.as_view(), name='korzinka_maxsulot')
]
urlpatterns += router.urls
