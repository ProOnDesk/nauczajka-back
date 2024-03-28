from .models import Tutor
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Tutor)
def validate_tutor(sender, instance, **kwargs):
    """
    Can't create a tutor instance if the user is not a tutor
    """
    if instance.user.is_tutor != True:
        raise ValidationError("Invalid tutor instance. The user must be a tutor.")