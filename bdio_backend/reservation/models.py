from django.db import models
from tutor.models import Tutor, TutorScheduleItems
from user.models import User


class TutoringReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='tutor_reservations')
    schedule_item = models.ManyToManyField(TutorScheduleItems, related_name='schedule_reservations')
    confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Reservation by {self.user.first_name} {self.user.last_name} with {self.tutor.user.first_name} {self.tutor.user.last_name}'
    
    def save(self, *args, **kwargs):
        if self.confirmed:
            self.schedule_item.is_reserved = True 
            
            