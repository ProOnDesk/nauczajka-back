from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from notification.serializers import NotificationSerializer
from notification.models import Notification
from notification.tasks import send_personal_notification_task
from rest_framework.response import Response


class NotificationListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(users=self.request.user).order_by('-created_at')
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        send_personal_notification_task.delay(user_id=self.request.user.id, message="Wlasnie poprosiles o historie twoich powiadomien :)")
        return Response(serializer.data)
    