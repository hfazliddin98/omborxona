from django.urls import path
from rest_framework.routers import SimpleRouter
# from .views import KategoriyaViewSet, MaxsulotViewSet, BirlikViewSet, OmborniYopishViewSet, OmborViewSet
# from .views import KorzinkaViewSet, OlinganMaxsulotlarViewSet, BuyurtmaViewSet, BuyurtmaSearchView
# from .views import JamiMahsulotViewSet, RadEtilganMaxsulotlarViewSet, TalabnomaViewSet
from ombor import views


router = SimpleRouter()
router.register(r'kategoriya', views.KategoriyaViewSet, basename='kategoriya')
router.register(r'maxsulot', views.MaxsulotViewSet, basename='maxsulot')
router.register(r'birlik', views.BirlikViewSet, basename='birlik')
router.register(r'omborni_yopish', views.OmborniYopishViewSet, basename='omborni_yopish')
router.register(r'ombor', views.OmborViewSet, basename='ombor')
router.register(r'buyurtma', views.BuyurtmaViewSet, basename='buyurtma')
router.register(r'buyurtma_maxsulot', views.BuyurtmaMaxsulotViewSet, basename='buyurtma_maxsulot')
router.register(r'korzinka', views.KorzinkaViewSet, basename='korzinka')
router.register(r'korzinka_maxsulot', views.KorzinkaMaxsulotViewSet, basename='korzinka_maxsulot')
router.register(r'olingan_maxsulotlar', views.OlinganMaxsulotlarViewSet, basename='olingan_maxsulotlar')
router.register(r'rad_etilgan_maxsulotlar', views.RadEtilganMaxsulotlarViewSet, basename='rad_etilgan_maxsulotlar')
router.register(r'jami_maxsulotlar', views.JamiMahsulotViewSet, basename='jami_maxsulotlar')
router.register(r'talabnoma', views.TalabnomaViewSet, basename='talabnoma')


urlpatterns = [
    path('buyurtma_search/', views.BuyurtmaSearchView.as_view(), name='buyurtma_search'),
]
urlpatterns += router.urls
