from django.contrib import admin
from notification.models import Notification, UserNotification, UserChatNotification

admin.site.register(Notification)
admin.site.register(UserNotification)
admin.site.register(UserChatNotification)