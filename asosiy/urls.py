from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from users.views import bosh_sahifa





urlpatterns = [
   path('haker/', admin.site.urls),
   path('', bosh_sahifa, name='bosh_sahifa'),
   path('api/token/', TokenObtainPairView.as_view(), name='token'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('ombor/', include('ombor.urls')),
   path('users/', include('users.urls')),
  

    # Optional UI:
   path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
   path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
   path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)