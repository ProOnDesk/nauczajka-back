from tutor.views import (
    TutorSkillsView,
    SkillsListView,
    TutorViewSet,
    TutorListView,
    TutorDetailView,
    DeleteTutorMeScheduleItemView,
    RetrieveCreateTutorMeScheduleItemsView,
    TutorMeView,
    TutorReviewView,
    TutorScheduleItemView
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'tutor'

router = DefaultRouter()
router.register(r'all', TutorViewSet, basename='tutors')

urlpatterns = [
    path('skills/me/', TutorSkillsView.as_view(), name='skills_me'),
    path('skills/', SkillsListView.as_view(), name='skills_list'),
    path('schedule/me/', RetrieveCreateTutorMeScheduleItemsView.as_view(), name='schedule_me'),
    path('schedule/me/<int:id>/', DeleteTutorMeScheduleItemView.as_view(), name='schedule_me_delete'),
    path('details/<int:id>/', TutorDetailView.as_view(), name='tutor_details'),
    path('reviews/<int:tutor_id>', TutorReviewView.as_view(), name='tutor_review'),
    path('schedule/<int:tutor_id>', TutorScheduleItemView.as_view(), name='tutor_schedule-item'),
    path('search/', TutorListView.as_view(), name='tutor_search'),
    path('me/', TutorMeView.as_view(), name='me'),
    path('', include(router.urls)),
]
