from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django_filters import rest_framework as filters
from .models import Tutor

class TutorFilter(filters.FilterSet):
    search_by_full_name = filters.CharFilter(method='filter_by_full_name')

    def filter_by_full_name(self, queryset, name, value):
        queryset = queryset.annotate(
            full_name=Concat('user__first_name', Value(' '), 'user__last_name', output_field=CharField())
        )
        return queryset.filter(full_name__icontains=value)

    class Meta:
        model = Tutor
        fields = {
            'avg_rating': ['lt', 'gt'],
            'skills': ['exact'],
        }
