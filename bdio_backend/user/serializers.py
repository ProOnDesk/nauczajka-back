from .models import User, TokenEmailConfirmation, Tutor

from rest_framework.serializers import ModelSerializer, ValidationError


class UserSerializer(ModelSerializer):
    """
    Serializer for the user object
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'is_tutor')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8
            }
        }

    def validate_email(self, email):
        """
        Validate the email field based on the is_tutor value
        """
        if self.initial_data.get('is_tutor') and (not email.endswith('@stud.prz.edu.pl') and not email.endswith('@prz.edu.pl')):
            raise ValidationError("Email must end with @stud.prz.edu.pl or @prz.edu.pl for tutors")
        return email
        
    
    def create(self, validated_data):
        """
        Create a new user with encrypted password and return it
        """
        return User.objects.create_user(**validated_data)
    

class TutorDescriptionSerializer(ModelSerializer):
    """
    Serializer for the tutor description object
    """
    class Meta:
        model = Tutor
        fields = ('description',)


class TokenEmailConfirmationSerializer(ModelSerializer):
    """
    Serializer for the token email confirmation object
    """
    class Meta:
        model = TokenEmailConfirmation
        fields = ('token',)
