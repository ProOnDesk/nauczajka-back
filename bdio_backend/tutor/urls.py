from .views import (
    TutorDescriptionView,
    TutorSkillsView,
    SkillsListView,
    TutorViewSet,
    TutorDetailView,
    DeleteTutorMeScheduleItemsView,
    RetrieveCreateTutorMeScheduleItemsView,
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'tutor'

router = DefaultRouter()
router.register(r'all', TutorViewSet, basename='tutor')


urlpatterns = [
    path('description/me/', TutorDescriptionView.as_view(), name='create'),
    path('skills/me/', TutorSkillsView.as_view(), name='skills-me'),
    path('skills/', SkillsListView.as_view(), name='skills-list'),
    path('schedule/me/', RetrieveCreateTutorMeScheduleItemsView.as_view(), name='schedule-me'),
    path('schedule/me/<int:id>', DeleteTutorMeScheduleItemsView.as_view(), name='schedule-me-delete'),
    path('all/details/<int:id>', TutorDetailView.as_view(), name='tutor-details'),
    path('', include(router.urls)),
]