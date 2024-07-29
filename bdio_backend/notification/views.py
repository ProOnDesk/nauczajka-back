from django.shortcuts import render
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from notification.serializers import UserNotificationSerializer, NotificationIsReadSerializer
from notification.models import UserNotification
from notification.utils import send_notification
from rest_framework.response import Response
from user.models import User
from core.pagination import CustomPagination


class NotificationListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return UserNotification.objects.filter(user=self.request.user).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        send_notification(users=self.request.user, message="Wlasnie poprosiles o historie twoich powiadomien :)")
        return response
    
    
class NotificationIsReadAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationIsReadSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        return UserNotification.objects.filter(user=self.request.user)