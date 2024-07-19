from rest_framework import serializers
from notification.models import UserNotification, Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('message',)
        read_only_fields = ('message',)



class UserNotificationSerializer(serializers.ModelSerializer):
    
    notification = NotificationSerializer()
    
    class Meta:
        model = UserNotification
        exclude  = ['user']


class NotificationIsReadSerializer(serializers.ModelSerializer):
    
    notification = NotificationSerializer(read_only=True)
    
    class Meta:
        model = UserNotification
        exclude  = ['user']
        extra_kwargs = {
            'user': {'read_only': False},
            'created_at': {'read_only': True},
            'user': {'read_only': True}
        }
        