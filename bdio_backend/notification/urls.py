from django.urls import include, path
from notification.views import NotificationListAPIView

urlpatterns = [
    path("list/", NotificationListAPIView.as_view(), name="notification_list")
]
