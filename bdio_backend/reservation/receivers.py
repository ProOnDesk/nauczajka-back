from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from reservation.models import TutoringReservation
from notification.utils import send_notification
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from reservation.models import TutoringReservation
from notification.models import Notification, UserNotification
from notification.utils import send_notification

@receiver(post_save, sender=TutoringReservation)
def notify_tutor_about_reservation(sender, instance, created, **kwargs):
    if created:
        message = f'{instance.user.first_name} {instance.user.last_name} zarezerwował/a korepetycje na {instance.schedule_item.start_time.strftime("%Y-%m-%d %H:%M:%S")}'
        
        notification = Notification.objects.create(message=message)
        user_notification = UserNotification.objects.create(user=instance.tutor.user, notification=notification)
        user_notification.save()