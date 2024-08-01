from django.urls import include, path
from reservation.views import (
    ReservationCreateAPIView,
    ReservationTutorMeAPIView,
    ReservationUserMeAPIView,
    ReservationTutorMeConfirmAPIView,
)

app_name = 'reservation'

urlpatterns = [
    path('reservation/', ReservationCreateAPIView.as_view(), name='reservation'),
    path('reservation/tutor/me/', ReservationTutorMeAPIView.as_view(), name='reservation_tutor_me'),
    path('reservation/user/me/', ReservationUserMeAPIView.as_view(), name='reservation_user_me'),
    path('reservation/tutor/me/confirm/<int:id>/', ReservationTutorMeConfirmAPIView.as_view(), name='reservation_tutor_me_confirm'),
]
