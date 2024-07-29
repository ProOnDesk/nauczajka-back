from django.db import models
from tutor.models import Tutor, TutorScheduleItems
from user.models import User
from django.core.exceptions import ValidationError
from datetime import datetime

class TutoringReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='tutor_reservations')
    schedule_item = models.ForeignKey(TutorScheduleItems, related_name='schedule_reservations', on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        unique_together = ('user', 'schedule_item')
    
    def __str__(self):
        return f'Reservation by {self.user.first_name} {self.user.last_name} with {self.tutor.user.first_name} {self.tutor.user.last_name}'
    
    def clean(self):
        if TutoringReservation.objects.filter(user=self.user, schedule_item=self.schedule_item).exists():
            raise ValidationError('This schedule item is already reserved for this user.')
        super().clean(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        if self.is_confirmed:
            self.schedule_item.is_reserved = True 
            self.schedule_item.save() 
        super().save(*args, **kwargs)
        