from django.urls import path
from .views import UserViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'users', UserViewSet)


urlpatterns = []
urlpatterns += router.urls
