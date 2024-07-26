from rest_framework import serializers
from chat.models import Conversation, ConversationMessage
from user.models import User
from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema_field
from typing import Optional

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user object
    """    
    profile_image = serializers.SerializerMethodField()
    
    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_profile_image(self, obj):
        if hasattr(obj, 'oauth2_picture') and obj.oauth2_picture.view_picture and obj.oauth2_picture.picture_url != "":
            return obj.oauth2_picture.picture_url
        
        if obj.profile_image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.profile_image.url)

        return None
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'profile_image')
        extra_kwargs = {
            'id': {'read_only': False},
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
            'profile_image': {'read_only': True},
        }

class ConversationMessagesSerializer(serializers.ModelSerializer):
    """
    Serializer for the conversation message object
    """
    created_by = UserSerializer()

    class Meta:
        model = ConversationMessage
        fields = ('id', 'conversation', 'body', 'created_at', 'created_by', 'file')
        extra_kwargs = {
            'id': {'read_only': True},
            'conversation': {'read_only': True},
            'created_at': {'read_only': True},
            'username': {'read_only': True},
        }
        ordering = ['-created_at']

    def to_representation(self, instance):
        # Pass context to the nested serializer
        representation = super().to_representation(instance)
        representation['created_by'] = UserSerializer(instance.created_by, context=self.context).data
        return representation

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
            'last_message': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True}
        }
    
    def get_last_message(self, obj) -> Optional[dict]:
        last_message = ConversationMessage.objects.filter(conversation=obj).order_by('-created_at').first()
        if last_message:
            return ConversationMessagesSerializer(last_message, context=self.context).data
        return None

    def create(self, validated_data):
        users_data = validated_data.pop('users')
        conversation = Conversation.objects.filter(users__id=users_data[0]['id']).filter(users__id=users_data[1]['id']).first()
        if conversation:
            return conversation
        conversation = Conversation.objects.create(created_by=self.context['request'].user ,**validated_data)
        
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
        
        return value
    
    def to_representation(self, instance):
        """
        Override the default to_representation method to insert the current user at the beginning of the users list
        """
        data = super().to_representation(instance)
        users_list = data.pop('users')

        new_users_list = []

        for user in users_list:
            if str(user['id']) == str(self.context['request'].user.id):
                new_users_list.insert(0, user)
            else:
                new_users_list.append(user)

        data['users'] = new_users_list
        return data


class UploadConversationMessageFileSerializer(serializers.ModelSerializer):
    """
    Serializer for the file message object
    """
    
    
    class Meta:
        model = ConversationMessage
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'body': {'read_only': True},
            'created_at': {'read_only': True},
            'created_by': {'read_only': True},
        }
        
        
    def create(self, validated_data):
        """
        Create a conversation
        """
        user = self.context['user']
        body_file_name = validated_data['file'].name
        
        conversation_message = ConversationMessage.objects.create(
            created_by=user, 
            body=body_file_name,
            **validated_data
            )
        
        return conversation_message
    