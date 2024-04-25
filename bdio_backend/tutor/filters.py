from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django_filters import rest_framework as filters
from .models import Tutor

class TutorFilter(filters.FilterSet):
    search_by_full_name = filters.CharFilter(method='filter_by_full_name')
    tutoring_location = filters.CharFilter(method='filter_by_location')
    
    def filter_by_full_name(self, queryset, name, value):
        queryset = queryset.annotate(
            full_name=Concat('user__first_name', Value(' '), 'user__last_name', output_field=CharField())
        )
        return queryset.filter(full_name__icontains=value)
    
    def filter_by_location(self, queryset, name, value):
        return queryset.filter(tutoring_location__istartswith=value)
        
    class Meta:
        model = Tutor
        fields = {
            'avg_rating': ['lt', 'gt'],
            'skills': ['exact'],
            'price': ['lt', 'gt'],
            'online_sessions_available': ['exact'],
            'in_person_sessions_available': ['exact'],
            'individual_sessions_available': ['exact'],
            'group_sessions_available': ['exact'],
        }
