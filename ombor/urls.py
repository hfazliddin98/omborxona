from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import KategoriyaViewSet, MaxsulotNomiViewSet, BirlikViewSet, OmborniYopishViewSet, OmborViewSet

router = SimpleRouter()
router.register(r'kategoriya', KategoriyaViewSet, basename='kategoriya')
router.register(r'mahsulot_nomi', MaxsulotNomiViewSet, basename='mahsulot_nomi')
router.register(r'birlik', BirlikViewSet, basename='birlik')
router.register(r'omborni_yopish', OmborniYopishViewSet, basename='omborni_yopish')
router.register(r'ombor', OmborViewSet, basename='ombor')


urlpatterns = []
urlpatterns += router.urls
