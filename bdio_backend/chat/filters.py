from django_filters import rest_framework as filters
from chat.models import Conversation, ConversationMessage


class ConversationMessageFilter(filters.FilterSet):

    number_of_last_messages = filters.NumberFilter(method='filter_by_number_of_last_messages')
    
    def filter_by_number_of_last_messages(self, queryset, name, value):
        return queryset.order_by('-created_at')[:value]
    
    class Meta:
        model = ConversationMessage
        fields = {}
