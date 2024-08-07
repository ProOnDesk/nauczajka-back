from django.db import models
from user.models import User

class Notification(models.Model):
    message = models.TextField()
    
    def __str__(self):
        if len(self.message) > 80:
            message = f'{self.message[0:80]}...'
        else:
            message = self.message
            
        return message


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications')
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='user_notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'notification')
        
    def __str__(self):
        if len(self.notification.message) > 80:
            notification = f'{self.notification.message[0:80]}...'
        else:
            notification = self.notification.message
            
        return f'{self.user.email} - {notification}'


class UserChatNotification(models.Model):
    user_notification = models.OneToOneField(UserNotification, on_delete=models.SET_NULL, null=True, related_name='chat_notification')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)