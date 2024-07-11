from .views import (
    TutorSkillsView,
    SkillsListView,
    TutorViewSet,
    TutorListView,
    TutorDetailView,
    DeleteTutorMeScheduleItemView,
    RetrieveCreateTutorMeScheduleItemsView,
    TutorMeView,
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'tutor'

router = DefaultRouter()
router.register(r'all', TutorViewSet, basename='tutors')

urlpatterns = [
    path('skills/me/', TutorSkillsView.as_view(), name='skills-me'),
    path('skills/', SkillsListView.as_view(), name='skills-list'),
    path('schedule/me/', RetrieveCreateTutorMeScheduleItemsView.as_view(), name='schedule-me'),
    path('schedule/me/<int:id>/', DeleteTutorMeScheduleItemView.as_view(), name='schedule-me-delete'),
    path('details/<int:id>/', TutorDetailView.as_view(), name='tutor-details'),
    path('search/', TutorListView.as_view(), name='tutor-search'),
    path('me/', TutorMeView.as_view(), name='me'),
    path('', include(router.urls)),
]
