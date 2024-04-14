from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from chat.models import Conversation, ConversationMessage
from chat.serializers import ConversationSerializer, ConversationMessagesSerializer
from drf_spectacular.utils import extend_schema


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
        serializer = self.serializer_class(data=data)
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
        return self.request.user.conversations.all()


@extend_schema(tags=['Chat'])
class ConversationDetailAPIView(APIView):
    
    serializer_class = ConversationMessagesSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        conversation = Conversation.objects.get(id=id)
        messages = ConversationMessage.objects.filter(conversation=conversation)
        serializer = ConversationMessagesSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)