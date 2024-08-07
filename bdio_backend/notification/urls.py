from django.urls import include, path
from notification.views import NotificationListAPIView, NotificationIsReadAPIView

urlpatterns = [
    path('list/', NotificationListAPIView.as_view(), name='notification_list'),
    path('is_read/<int:id>/', NotificationIsReadAPIView.as_view(), name='notification_is_read')
]
