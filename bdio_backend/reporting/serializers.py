from rest_framework import serializers
from reporting.models import Issue, Respond

class IssueSerializer(serializers.ModelSerializer):
    """
    Issue Serializer
    """
    
    
    class Meta:
        model = Issue
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'reported_by': {'read_only': True},
            'status': {'read_only': True},
        }
        
    def create(self, validated_data):
        """
        Create a user issue
        """
        user = self.context.get('user')
        issue = Issue.objects.create(reported_by=user, **validated_data)
        
        return issue    

class RespondSerializer(serializers.ModelSerializer):
    """
    Respond Serialzer
    """
    
    
    class Meta:
        model = Respond
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'issue': {'read_only': True},
            'responder': {'read_only': True},
        }
        
class IssueDetailSerializer(serializers.ModelSerializer):
    """
    Issue Serializer
    """
    responds =  RespondSerializer(many=True, read_only=True)
    
    
    class Meta:
        model = Issue
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'reported_by': {'read_only': True},
            'status': {'read_only': True},
            'responds': {'read_only': True},
        }
