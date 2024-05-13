from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django_filters import rest_framework as filters
from .models import Tutor

class TutorFilter(filters.FilterSet):
    search_by_full_name = filters.CharFilter(method='filter_by_full_name')
    tutoring_location = filters.CharFilter(method='filter_by_location')
    sorting_by_hourly_rate = filters.CharFilter(method='filter_by_hourly_rate')
    sorting_by_average_rating = filters.CharFilter(method='filter_by_average_rating')

    def filter_by_full_name(self, queryset, name, value):
        queryset = queryset.annotate(
            full_name=Concat('user__first_name', Value(' '), 'user__last_name', output_field=CharField())
        )
        return queryset.filter(full_name__icontains=value)
    
    def filter_by_location(self, queryset, name, value):
        return queryset.filter(tutoring_location__istartswith=value)
    
    def filter_by_hourly_rate(self, queryset, name, value):
        if value.lower() == 'asc':
            return queryset.order_by('price')
        elif value.lower() == 'desc':
            return queryset.order_by('-price')
        else:
            return queryset
        
    def filter_by_average_rating(self, queryset, name, value):
        if value.lower() == 'asc':
            return queryset.order_by('avg_rating')
        elif value.lower() == 'desc':
            return queryset.order_by('-avg_rating')
        else:
            return queryset
        
    class Meta:
        model = Tutor
        fields = {
            'avg_rating': ['lt', 'gt','lte', 'gte'],
            'skills': ['exact'],
            'price': ['lt', 'gt', 'lte', 'gte'],
            'online_sessions_available': ['exact'],
            'in_person_sessions_available': ['exact'],
            'individual_sessions_available': ['exact'],
            'group_sessions_available': ['exact'],
        }
