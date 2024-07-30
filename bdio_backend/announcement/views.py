from rest_framework import response, status, generics
from announcement.serializers import AnnouncementSerializer
from rest_framework.permissions import IsAuthenticated
from announcement.models import Announcement
from drf_spectacular.utils import extend_schema
from core.pagination import CustomPagination
from tutor.permissions import IsTutor


@extend_schema(tags=['Announcement'])
class AnnouncementListAPIView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all().order_by('-created_at')
    pagination_class = CustomPagination    
    
    
@extend_schema(tags=['Announcement'])
class AnnouncementCreateAPIView(generics.CreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated, IsTutor]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    