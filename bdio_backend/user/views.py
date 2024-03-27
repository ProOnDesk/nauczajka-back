from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsTutor
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings

from .serializers import (
    UserSerializer,
    TokenEmailConfirmationSerializer,
    TutorDescriptionSerializer,
    UserImageProfileSerializer,
)

from .models import TokenEmailConfirmation, User

class CreateUserView(APIView):
    """
    Create a new user
    """
    serializer_class = UserSerializer
    
    def post(self, request):
        """
        Create a new user
        """
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()
                return Response({"Info": "Your confirmation account was send to your email"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            if serializer.is_valid():
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
class ProfileUserView(APIView):
    """
    View and update user profile
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    
    def get(self, request):
        """
        Get user profile
        """
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        """
        Update user profile
        """
        serializer = self.serializer_class(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ConfirmUserView(APIView):
    """
    Confirm user account via email
    """
    
    serializer_class = TokenEmailConfirmationSerializer
    
    def post(self, request):
        """
        Confirm account via email containing token
        """
        token = request.data.get('token')
        
        if not token:
            return Response({"Error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token_email_confirmation = TokenEmailConfirmation.objects.get(token=token)
        except TokenEmailConfirmation.DoesNotExist:
            return Response({"Error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
        # if is_token_expired(token_email_confirmation):
        #     return Response({"Error": "Token is expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(email=token_email_confirmation.user.email)
        if user.is_confirmed:
            return Response({"Error": "User is already confirmed"}, status=status.HTTP_400_BAD_REQUEST)
        user.is_confirmed = True
        user.save()
        token_email_confirmation.delete()
        
        return Response({"Info": "Email confirmed"}, status=status.HTTP_200_OK)
        

class ProfileImageView(APIView):
    """
    Upload and delete user profile image
    """
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserImageProfileSerializer
    
    def patch(self, request):
        """
        Upload user profile image
        """
        serializer = self.serializer_class(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        """
        Delete user profile image
        """
        user = request.user
        if user.profile_image.name == settings.DEFAULT_USER_PROFILE_IMAGE:
            return Response({"Error": "User has no profile image"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.profile_image.delete()
        user.profile_image = settings.DEFAULT_USER_PROFILE_IMAGE
        user.save()
        return Response({"Info": "Image deleted."}, status=status.HTTP_200_OK)
    
class TutorDescriptionView(APIView):
    """
    View and update tutor description
    """
    permission_classes = (IsAuthenticated, IsTutor,)
    serializer_class = TutorDescriptionSerializer
    
    def get(self, request):
        """
        Get tutor description
        """
        serializer = self.serializer_class(request.user.tutor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        """
        Update tutor description
        """
        serializer = self.serializer_class(request.user.tutor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)