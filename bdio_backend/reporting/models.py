from django.db import models
from user.models import User
import uuid


class Issue(models.Model):
    CATEGORY_CHOICES = [
        ('naruszenie_regulaminu', 'Naruszenie Regulaminu'),
        ('problem_techniczny', 'Problem Techniczny'),
        ('prosba_o_pomoc', 'Prośba o Pomoc'),
    ]
    
    STATUS_CHOICES = [
        ('nowe', 'Nowe'),
        ('w_trakcie', 'W Trakcie'),
        ('rozwiazane', 'Rozwiązane'),
        ('zamkniete', 'Zamknięte'),
    ]
    
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_issues')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"{self.get_category_display()}: {self.title} ({self.get_status_display()})"


class Respond(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='responds')
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Respond to '{self.issue.title}' by {self.responder.first_name} {self.responder.last_name}"
