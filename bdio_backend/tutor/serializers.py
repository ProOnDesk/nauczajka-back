from .models import Tutor
from rest_framework.serializers import ModelSerializer

class TutorDescriptionSerializer(ModelSerializer):
    """
    Serializer for the tutor description object
    """
    class Meta:
        model = Tutor
        fields = ('description',)