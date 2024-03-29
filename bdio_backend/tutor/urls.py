from .views import (
    TutorDescriptionView,
    TutorSkillsView,
    SkillsListView,
)
from django.urls import path

app_name = 'tutor'

urlpatterns = [
    path('description/me', TutorDescriptionView.as_view(), name='create'),
    path('skills/me', TutorSkillsView.as_view(), name='skills-me'),
    path('skills/', SkillsListView.as_view(), name='skills-list'),
]