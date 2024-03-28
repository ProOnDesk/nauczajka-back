from .views import (
    TutorDescriptionView,
)
from django.urls import path

app_name = 'tutor'

urlpatterns = [
    path('description/', TutorDescriptionView.as_view(), name='create'),
]