"""
MAIN URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/swagger/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('api/', include('api.urls')),
    path('api/user/', include('user.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/reporting/', include('reporting.urls')),
    path('api/notification/', include('notification.urls')),
    path('api/reservation/', include('reservation.urls')),
    path('api/announcement/', include('announcement.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
