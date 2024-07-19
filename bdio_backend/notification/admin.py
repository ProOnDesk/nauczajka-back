from django.contrib import admin
from notification.models import Notification, UserNotification

admin.site.register(Notification)
admin.site.register(UserNotification)