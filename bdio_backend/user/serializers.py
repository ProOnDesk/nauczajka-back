from .models import User

from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    """
    Serializer for the user object
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8
            }
        }

    def create(self, validated_data):
        """
        Create a new user with encrypted password and return it
        """
        return User.objects.create_user(**validated_data)
