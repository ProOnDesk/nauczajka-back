from django.db import models
from user.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Tutor(models.Model):
    """
    Tutor model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField('Skills', related_name='tutors')
    price = models.IntegerField(default=0)
    online_sessions_available = models.BooleanField(default=False)
    in_person_sessions_available = models.BooleanField(default=False)
    tutoring_location = models.CharField(max_length=100, blank=True, null=True)
    individual_sessions_available = models.BooleanField(default=False)
    group_sessions_available = models.BooleanField(default=False)

    avg_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)

    def __str__(self):
        return f"Tutor - {self.user.email}"
    

class Skills(models.Model):
    """
    Skills model
    """
    skill = models.CharField(max_length=100, primary_key=True, unique=True)

    def __str__(self):
        return f"Skill - {self.skill}"


class TutorScheduleItems(models.Model):
    """
    ScheduleItems model
    """
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='tutor_schedule_items')
    start_time = models.DateTimeField(help_text="Format: YYYY-MM-DD HH:MM:SS")
    end_time = models.DateTimeField(help_text="Format: YYYY-MM-DD HH:MM:SS")
    
    def __str__(self):
        return f"ScheduleItem - {self.tutor.user.email} - {self.start_time} - {self.end_time}"
    
    def clean(self):
        """
        Walidacja zakresu czasowego, aby uniknąć nakładających się terminów.
        """
        # Sprawdź czy start_time nie jest późniejszy niż end_time
        if self.start_time >= self.end_time:
            raise ValidationError("Czas rozpoczęcia musi być wcześniejszy niż czas zakończenia.")
        
        # Sprawdź czy istnieją już inne TutorScheduleItems nakładające się na ten przedział czasowy
        overlapping_items = TutorScheduleItems.objects.filter(
            tutor=self.tutor,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)  # Wyklucz aktualny obiekt z wyników, gdy edytujemy istniejący obiekt
        
        if overlapping_items.exists():
            raise ValidationError(_("Your schedule is overlapping with another schedule."))
    
    
class TutorRatings(models.Model):
    """
    Tutors ratings model
    """
    id = models.AutoField(primary_key=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='tutor_ratings')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_ratings')
    rating = models.SmallIntegerField(default=5)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Rating - {self.rating} for tutor({self.tutor.user.email}) from ({self.student.email}) "
    
    def validate_unique(self, *args, **kwargs):
        super().validate_unique(*args, **kwargs)
        if TutorRatings.objects.filter(tutor=self.tutor, student=self.student).exists():
            raise ValidationError(_("You have already rated this tutor."))