from .models import User, TokenEmailConfirmation, Tutor

from rest_framework.serializers import ModelSerializer, ValidationError

    
class CreateUserSerializer(ModelSerializer):
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
   
    
class UserUpdateSerializer(ModelSerializer):
    """
    Serializer for the user profile update object
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'profile_image', 'password', 'is_tutor', 'created_at')
        extra_kwargs = {
            'profile_image': {
                'read_only': True
            },
            'password': {
                'write_only': True,
                'min_length': 8
            },
            'email': {
                'read_only': True
            },
            'is_tutor': {
                'read_only': True
            },
            'created_at': {
                'read_only': True
            }
        }
        
    def update(self, instance, validated_data):
        """
        Update a user, setting the password correctly and return it
        """
        password = validated_data.pop('password', None)
        
        user = super().update(instance, validated_data)
        
        if password:
            user.set_password(password)
            user.save()
        return user
    

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
        
class UserImageProfileSerializer(ModelSerializer):
    """
    Serializer for the user image profile object
    """
    class Meta:
        model = User
        fields = ('profile_image',)
        
    def update(self, instance, validated_data):
        """Update a user, setting the image correctly and return it."""
        image = validated_data.pop('image', None)

        user = super().update(instance, validated_data)

        if image:
            user.image = image
            user.save()
        return user
