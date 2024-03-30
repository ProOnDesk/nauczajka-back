from django.db import models
from user.models import User

class Tutor(models.Model):
    """
    Tutor model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField('Skills', related_name='tutors')
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
    
    
class TutorRatings(models.Model):
    """
    Tutors ratings model
    """
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='tutor_ratings')
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_rating')
    rating = models.SmallIntegerField(default=5)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Rating - {self.rating} for tutor({self.tutor.user.email}) from ({self.student.email}) "