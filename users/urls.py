from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, BinosViewSet

router = SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'binos', BinosViewSet)


urlpatterns = []
urlpatterns += router.urls
