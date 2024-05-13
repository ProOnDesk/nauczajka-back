from .models import Tutor, TutorRatings
from chat.models import ConversationMessage
from django.db.models.signals import pre_save, post_save, post_delete
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
@receiver(post_delete, sender=TutorRatings)
def update_tutor_avg_rating(sender, instance, **kwargs):
    """
    Signal to update the average rating for the tutor whenever a new rating is added or deleted
    """
    tutor = instance.tutor
    avg_rating = TutorRatings.objects.filter(tutor=tutor).aggregate(Avg('rating'))['rating__avg']
    tutor.avg_rating = avg_rating if avg_rating else 0
    tutor.save()
    print("cos sie wyknoalo")
    
@receiver(pre_save, sender=ConversationMessage)
def update_conversation_updated_at(sender, instance, **kwargs):
    instance.conversation.updated_at = instance.created_at  
    instance.conversation.save()
