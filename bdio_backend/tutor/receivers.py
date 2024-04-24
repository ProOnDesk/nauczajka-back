from .models import Tutor, TutorRatings
from chat.models import ConversationMessage
from django.db.models.signals import pre_save, post_save
from django.db.models import Avg
from django.dispatch import receiver
from django.core.exceptions import ValidationError

@receiver(pre_save, sender=Tutor)
def validate_tutor(sender, instance, **kwargs):
    """
    Can't create a tutor instance if the user is not a tutor
    """
    if instance.user.is_tutor != True:
        raise ValidationError("Invalid tutor instance. The user must be a tutor.")
    
@receiver(post_save, sender=TutorRatings)
def update_tutor_avg_rating(sender, instance, **kwargs):
    """
    Signal to update the average rating for the tutor whenever a new rating is added
    """
    tutor = instance.tutor
    avg_rating = TutorRatings.objects.filter(tutor=tutor).aggregate(Avg('rating'))['rating__avg']
    tutor.avg_rating = avg_rating if avg_rating else 0
    tutor.save()
    
@receiver(pre_save, sender=ConversationMessage)
def update_conversation_updated_at(sender, instance, **kwargs):
    instance.conversation.updated_at = instance.created_at  
    instance.conversation.save()
    print(f"Conversation updated at. {instance.conversation.updated_at}")