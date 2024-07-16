from user.models import User, TokenEmailConfirmation, User_Oauth2_Picture
from tutor.models import TutorRatings
from rest_framework.serializers import ModelSerializer, ValidationError, CharField, SerializerMethodField
from django.utils.translation import gettext as _

class UserSerializer(ModelSerializer):
    """
    Serializer for the user object
    """
    profile_image = SerializerMethodField()
    
    def get_profile_image(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return None
    
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'profile_image', 'created_at')
        extra_kwargs = {
            'profile_image': {'read_only': True},
            'created_at': {'read_only': True}
        }    
        
        
class CreateUserSerializer(ModelSerializer):
    """
    Serializer for creating a new user object
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'is_tutor')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
        }

    def validate_email(self, email):
        """
        Validate the email field based on the is_tutor value
        """
        if self.initial_data.get('is_tutor') and not (email.endswith('@stud.prz.edu.pl') or email.endswith('@prz.edu.pl')):
            raise ValidationError(_("Email must end with @stud.prz.edu.pl or @prz.edu.pl for tutors"))
        return email
        
    def create(self, validated_data):
        """
        Create a new user with encrypted password and return it
        """
        return User.objects.create_user(**validated_data)
   
    
class UserUpdateSerializer(ModelSerializer):
    """
    Serializer for updating user profile
    """
    profile_image = SerializerMethodField()
    
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
        fields = ('id', 'email', 'first_name', 'last_name', 'profile_image', 'password', 'is_tutor', 'created_at')
        extra_kwargs = {
            'profile_image': {'read_only': True},
            'password': {'write_only': True, 'min_length': 8},
            'email': {'read_only': True},
            'is_tutor': {'read_only': True},
            'created_at': {'read_only': True},
            'id': {'read_only': True}
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
    

class TokenEmailConfirmationSerializer(ModelSerializer):
    """
    Serializer for the token email confirmation object
    """
    class Meta:
        model = TokenEmailConfirmation
        fields = ('token',)
  
  
class UserImageProfileSerializer(ModelSerializer):
    """
    Serializer for updating user profile image
    """
    class Meta:
        model = User
        fields = ('profile_image',)
        
    def get_profile_image(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.profile_image.url)

        return None    
        
    def update(self, instance, validated_data):
        """Update a user's profile image and return it."""
        image = validated_data.pop('image', None)

        user = super().update(instance, validated_data)

        if image:
            user.profile_image = image
            user.save()
        return user


class RateTutorSerializer(ModelSerializer):
    """
    Serializer for rating a tutor
    """
    class Meta:
        model = TutorRatings
        fields = ('rating', 'review', 'created_at')
        READ_ONLY_FIELDS = ('created_at',)

    def create(self, validated_data):
        """
        Rate a tutor and return it
        """
        user = self.context['user']
        tutor = self.context['tutor']
        
        if user == tutor.user:
            raise ValidationError(_("You can't rate yourself"))
        
        return TutorRatings.objects.create(student=user, tutor=tutor, **validated_data)

    def validate_rating(self, rating):
        """
        Validate the rating field
        """
        if rating < 1 or rating > 5:
            raise ValidationError(_("Rating must be between 1 and 5"))
        return rating


class RatingsMeSerializer(ModelSerializer):
    """
    Serializer for user ratings
    """
    tutor_id = CharField(source='tutor.id', read_only=True)

    class Meta:
        model = TutorRatings
        fields = ('rating', 'review', 'created_at','tutor_id')
        read_only_fields = ('created_at',)