from .views import (
    TutorDescriptionView,
    TutorSkillsView,
    SkillsListView,
    TutorViewSet,
    TutorListView,
    TutorPriceView,
    TutorDetailView,
    DeleteTutorMeScheduleItemView,
    RetrieveCreateTutorMeScheduleItemsView,
    TutorMethodSessionAvailabilityView,
    TutorMeView,
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'tutor'

router = DefaultRouter()
router.register(r'all', TutorViewSet, basename='tutors')

urlpatterns = [
    path('description/me/', TutorDescriptionView.as_view(), name='create'),
    path('price/me/', TutorPriceView.as_view(), name='price-me'),
    path('skills/me/', TutorSkillsView.as_view(), name='skills-me'),
    path('skills/', SkillsListView.as_view(), name='skills-list'),
    path('schedule/me/', RetrieveCreateTutorMeScheduleItemsView.as_view(), name='schedule-me'),
    path('schedule/me/<int:id>/', DeleteTutorMeScheduleItemView.as_view(), name='schedule-me-delete'),
    path('details/<int:id>/', TutorDetailView.as_view(), name='tutor-details'),
    path('search/', TutorListView.as_view(), name='tutor-search'),
    path('method_session_availability/me/', TutorMethodSessionAvailabilityView.as_view(), name='method-session-availability-me'),
    path('me/', TutorMeView.as_view(), name='me'),
    path('', include(router.urls)),
]
