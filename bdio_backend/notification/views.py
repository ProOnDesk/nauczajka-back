from django.shortcuts import render
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from notification.serializers import UserNotificationSerializer, NotificationIsReadSerializer
from notification.models import UserNotification
from notification.utils import send_notification
from rest_framework.response import Response
from user.models import User


class NotificationListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationSerializer
    
    def get_queryset(self):
        return UserNotification.objects.filter(user=self.request.user).order_by('-created_at')
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        send_notification(users=self.request.user, message="Wlasnie poprosiles o historie twoich powiadomien :)")
        return Response(serializer.data)
    
    
class NotificationIsReadAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationIsReadSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        return UserNotification.objects.filter(user=self.request.user)