from django.urls import path
from announcement.views import (
    AnnouncementListAPIView,
    AnnouncementCreateAPIView
)
app_name = 'announcement'

urlpatterns = [
    path('announcements/', AnnouncementListAPIView.as_view(), name='announcement_list'),
    path('announcement/', AnnouncementCreateAPIView.as_view(), name='announcement_create')
]
