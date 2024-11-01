from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import KategoriyaViewSet, MaxsulotViewSet, BirlikViewSet, OmborniYopishViewSet, OmborViewSet
from .views import KorzinkaViewSet, OlinganMaxsulotlarViewSet

router = SimpleRouter()
router.register(r'kategoriya', KategoriyaViewSet, basename='kategoriya')
router.register(r'mahsulot', MaxsulotViewSet, basename='mahsulot')
router.register(r'birlik', BirlikViewSet, basename='birlik')
router.register(r'omborni_yopish', OmborniYopishViewSet, basename='omborni_yopish')
router.register(r'ombor', OmborViewSet, basename='ombor')
router.register(r'korzinka', KorzinkaViewSet, basename='korzinka')
router.register(r'olingan_maxsulotlar', OlinganMaxsulotlarViewSet, basename='olingan_maxsulotlar')


urlpatterns = []
urlpatterns += router.urls
