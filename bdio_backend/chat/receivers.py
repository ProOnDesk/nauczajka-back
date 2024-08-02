from django.db.models.signals import post_save
from django.dispatch import receiver
from chat.models import Conversation, ConversationMessage, ConversationReadStatus
from chat.tasks import send_update_chat_to_channel_task, send_message_task
from notification.utils import send_notification
from notification.models import UserChatNotification, UserNotification

@receiver(post_save, sender=ConversationMessage)
def send_update_chat_to_channel(sender, instance, created, **kwargs):
    if created:
        send_update_chat_to_channel_task.delay(str(instance.conversation.id), str(instance.created_by.id))
        
@receiver(post_save, sender=ConversationMessage)
def send_message(sender, instance, created, **kwargs):
    if created:
        send_message_task(str(instance.id), f"chat_{instance.conversation.id}")
        

@receiver(post_save, sender=Conversation)
def update_read_status(sender, instance, created, **kwargs):
    if created:
        for user in instance.users.all():
            ConversationReadStatus.objects.create(
                user=user,
                conversation=instance,
                is_read=False  
            )
    else:
        for user in instance.users.all():
            read_status, created = ConversationReadStatus.objects.get_or_create(
                user=user,
                conversation=instance,
                defaults={'is_read': False}
            )
            if not created:
                if not read_status.is_connected_to_chat:

                    read_status.is_read = False
                    read_status.save()
                    count = ConversationReadStatus.objects.filter(user=user, is_read=False).count()
                    if count > 0:
                        print(count)
                        user_chat_notification, created = UserChatNotification.objects.get_or_create(user=user)
                        
                        if not created:
                            user_notification = user_chat_notification.user_notification
                            notification = user_notification.notification
                            if count == 1:
                                notification.message = f'Masz {count} nieprzeczytaną wiadomość'
                            else:
                                notification.message = f'Masz {count} nieprzeczytanych wiadomości od różnych osób'

                            notification.save()
                            user_notification.delete()
                            user_notification = UserNotification.objects.create(user=user, notification=notification)
                            user_chat_notification.user_notification = user_notification
                            user_chat_notification.save()
                    