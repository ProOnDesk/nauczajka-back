from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from chat.models import Conversation, ConversationMessage

from chat.serializers import (
    ConversationSerializer,
    ConversationMessagesSerializer,
    UploadConversationMessageFileSerializer
)
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django.utils.translation import gettext as _
from django.utils import timezone
from core.utils import get_profile_image_with_ouath2
from core.pagination import CustomPagination
from rest_framework.parsers import MultiPartParser, FormParser

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings


@extend_schema(tags=['Chat'])
class ConversationCreateAPIView(APIView):
    """
    Create a conversation
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer
    
    def post(self, request):
        data = request.data
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
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.request.user.conversations.order_by('-updated_at')
    


@extend_schema(tags=['Chat'])
class ConversationDetailAPIView(generics.ListAPIView):
    
    serializer_class = ConversationMessagesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    queryset = ConversationMessage.objects.all()
    pagination_class = CustomPagination

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


@extend_schema(tags=['Chat'])
class ConversationRetrieveAPIView(generics.RetrieveAPIView):
    """
    Retrieve a conversation by conversation id
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    def get_queryset(self):
        conversation_id = self.kwargs.get('id')
        return Conversation.objects.filter(users=self.request.user, id=conversation_id)
    

    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({'detail': _('Brak konwersacji')}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance)

        return Response(serializer.data)
     

@extend_schema(tags=['Chat'])
class UploadConversationMessageFileAPIView(APIView):
    """
    API view for uploading conversation message files.
    """
    serializer_class = UploadConversationMessageFileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user, 'request': request})
        
        if serializer.is_valid():
            message = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    