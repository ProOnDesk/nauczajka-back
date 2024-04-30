from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from chat.models import Conversation, ConversationMessage
from chat.serializers import ConversationSerializer, ConversationMessagesSerializer
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from chat.filters import ConversationMessageFilter
from rest_framework import generics
from django.utils.translation import gettext as _

@extend_schema(tags=['Chat'])
class ConversationCreateAPIView(APIView):
    """
    Create a conversation
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer
    
    def post(self, request):
        user_id = request.user.id
        data = request.data
        data['users'].append({'id': user_id})
        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Chat'])
class ConversationListAPIView(ListAPIView):
    """
    List all conversations
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.conversations.order_by('-updated_at')


@extend_schema(tags=['Chat'])
class ConversationDetailAPIView(generics.ListAPIView):
    
    serializer_class = ConversationMessagesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConversationMessageFilter
    queryset = ConversationMessage.objects.all()
    
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        conversation_id = self.kwargs.get('id')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            if self.request.user not in conversation.users.all():
                return queryset.none()
            return queryset.filter(conversation_id=conversation_id).order_by('created_at')
        except Conversation.DoesNotExist:
            return queryset.none()
