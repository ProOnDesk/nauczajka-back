from django_filters import rest_framework as filters
from reservation.models import TutoringReservation

class ReservationFilter(filters.FilterSet):

    class Meta:
        model = TutoringReservation
        fields = {
            'is_confirmed': ['exact']
        }