from django.urls import include, path
from reservation.views import ReservationCreateAPIView

urlpatterns = [
    path('reservation/', ReservationCreateAPIView.as_view(), name='reservation'),
    path('reservation/tutor/me/'),
    path('reservation/tutor/me/confirm'),
    path('reservation/user/me')
 
]
