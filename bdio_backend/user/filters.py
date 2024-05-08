from django_filters import rest_framework as filters
from tutor.models import TutorRatings


class RatingsFilter(filters.FilterSet):

    number_of_ratings = filters.NumberFilter(method='filter_by_number_of_ratings')
    
    def filter_by_number_of_ratings(self, queryset, name, value):
        return queryset[:value]
    
    class Meta:
        model = TutorRatings
        fields = {}
