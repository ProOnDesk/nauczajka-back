from rest_framework import serializers
from chat.models import Conversation, ConversationMessage
from user.models import User
from django.utils.translation import gettext as _
from operator import itemgetter
from typing import Optional



class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user object
    """
    
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'profile_image')
        extra_kwargs = {
            'id': {'read_only': False},
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
            'profile_image': {'read_only': True},
        }


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the conversation object
    """
    users = UserSerializer(many=True, required=True)
    last_message = serializers.SerializerMethodField()

    
    class Meta:
        model = Conversation
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'last_meesage': {'read_only': True},
            'updated_at': {'read_only': True},
        }
    
    def get_last_message(self, obj) -> Optional[dict]:
        last_message = ConversationMessage.objects.filter(conversation=obj).order_by('-created_at').first()
        if last_message:
            return ConversationMessagesSerializer(last_message).data
        return None
      
    def create(self, validated_data):
        users_data = validated_data.pop('users')
        conversation = Conversation.objects.create(**validated_data)
        
        for user_data in users_data:
            user = User.objects.get(id=user_data['id'])
            conversation.users.add(user)
        return conversation

    def validate_users(self, value):
        if len(value) != 2:
            raise serializers.ValidationError(_('Rozmowa musi mieć dokładnie dwóch użytkowników.'))
        
        if value[0]['id'] == value[1]['id']:
            raise serializers.ValidationError(_('Rozmowa musi mieć dwóch różnych użytkowników.'))
        
        if not User.objects.filter(id=value[0]['id']).exists() or not User.objects.filter(id=value[1]['id']).exists():
            raise serializers.ValidationError(_('Użytkownicy muszą istnieć.'))
        
        if Conversation.objects.filter(users__id=value[0]['id']).filter(users__id=value[1]['id']).exists():
            raise serializers.ValidationError(_('Rozmowa już istnieje.'))
        
        return value
            

class ConversationMessagesSerializer(serializers.ModelSerializer):
    """
    Serializer for the conversation message object
    """
    created_by = UserSerializer()
    
    
    class Meta:
        model = ConversationMessage
        fields = ('id', 'conversation', 'body', 'created_at', 'created_by')
        extra_kwargs = {
            'id': {'read_only': True},
            'conversation': {'read_only': True},
            'created_at': {'read_only': True},
            'username': {'read_only': True},
        }
        ordering = ['-created_at']
    