from django.urls import path, include

from chat.views import (
    ConversationListAPIView,
    ConversationCreateAPIView,
    ConversationDetailAPIView,
    ConversationRetrieveAPIView,
    UploadConversationMessageFileAPIView,
)

app_name = 'chat'
urlpatterns = [
    path('conversations/', ConversationListAPIView.as_view(), name='conversations'),
    path('conversation_detail/<uuid:id>/', ConversationDetailAPIView.as_view(), name='conversation'),
    path('conversation/', ConversationCreateAPIView.as_view(), name='create-conversation'),
    path('conversation/user/<uuid:id>/', ConversationRetrieveAPIView.as_view(), name='retrieve-conversation'),
    path('conversation/message/upload-file/', UploadConversationMessageFileAPIView.as_view(), name='upload_conversation_message_file')
]
