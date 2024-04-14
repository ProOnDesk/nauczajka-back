from django.urls import path, include

from .views import (
    ConversationListAPIView,
    ConversationCreateAPIView,
    ConversationDetailAPIView,
)

app_name = 'chat'
urlpatterns = [
    path('conversations/', ConversationListAPIView.as_view(), name='conversations'),
    path('conversation_detail/<uuid:id>/', ConversationDetailAPIView.as_view(), name='conversation'),
    path('conversation/', ConversationCreateAPIView.as_view(), name='create-conversation'),
]
