from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.utils.translation import gettext as _

from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from user.filters import RatingsFilter

from user.serializers import (
    CreateUserSerializer,
    TokenEmailConfirmationSerializer,
    UserImageProfileSerializer,
    UserUpdateSerializer,
    RateTutorSerializer,
    RatingsMeSerializer,
)

from .models import TokenEmailConfirmation, User, User_Oauth2_Picture
from tutor.models import Tutor, TutorRatings

class CreateUserView(APIView):
    """
    Create a new user
    """
    authentication_classes = []
    serializer_class = CreateUserSerializer
    
    def post(self, request):
        """
        Create a new user
        """
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()
                return Response({"Info": _("Your confirmation code was send to your email.")}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            if serializer.is_valid():
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(generics.DestroyAPIView):
    """
    Delete user account
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserUpdateSerializer

    def delete(self, request):
        """
        Delete user account
        """
        user = request.user
        user.delete()
        return Response({"Info": _("Account deleted successfully.")}, status=status.HTTP_200_OK)


@extend_schema(tags=['User Profile'])
class ProfileUserView(generics.RetrieveUpdateAPIView):
    """
    View and update user profile
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserUpdateSerializer
    
    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

    
class ConfirmUserView(APIView):
    """
    Confirm user account via email
    """
    authentication_classes = []
    serializer_class = TokenEmailConfirmationSerializer
    
    def post(self, request):
        """
        Confirm account via email containing token
        """
        token = request.data.get('token')
        
        if not token:
            return Response({"Error": _("Token is required.")}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token_email_confirmation = TokenEmailConfirmation.objects.get(token=token)
        except TokenEmailConfirmation.DoesNotExist:
            return Response({"Error": _("Invalid token.")}, status=status.HTTP_400_BAD_REQUEST)
        
        # if is_token_expired(token_email_confirmation):
        #     return Response({"Error": "Token is expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(email=token_email_confirmation.user.email)
        if user.is_confirmed:
            return Response({"Error": _("Account is already confirmed.")}, status=status.HTTP_400_BAD_REQUEST)
        user.is_confirmed = True
        user.save()
        token_email_confirmation.delete()
        
        return Response({"Info": _("Email confirmed.")}, status=status.HTTP_200_OK)
        

@extend_schema(tags=['User Profile'])
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
        serializer = self.serializer_class(request.user, data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                user_oauth_picture = User_Oauth2_Picture.objects.get(user=request.user)
            except User_Oauth2_Picture.DoesNotExist:
                user_oauth_picture = None
            
            if user_oauth_picture is not None:
                user_oauth_picture.view_picture = False
                user_oauth_picture.picture_url = ""
                user_oauth_picture.save()
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        """
        Delete user profile image
        """
        user = request.user
        if user.profile_image.name == settings.DEFAULT_USER_PROFILE_IMAGE:
            return Response({"Error": _("Account has no profile image")}, status=status.HTTP_400_BAD_REQUEST)
        
        user.profile_image.delete()
        user.profile_image = settings.DEFAULT_USER_PROFILE_IMAGE
        user.save()
        return Response({"Info": _("Profile image deleted.")}, status=status.HTTP_200_OK)


class CheckUserPasswordView(APIView):
    """
    Check user password
    """
    permission_classes = (IsAuthenticated,)
    @extend_schema(
        request={
            "application/json": {
                "example": {"password": "example123"},
            }
        },
        responses={
            200: {"example": {'password_matches': True},
                  "example": {'password_matches': False}},
            400: {"example": {'error': _('Password is required.')}},
        },
        description=_("Check if the provided password matches the authenticated user's password.")
    )
    def post(self, request):
        """
        Check user password
        """
        password = request.data.get('password')
        if not password:
            return Response({"Error": _("Password is required.")}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        if not user.check_password(password):
            return Response({"password_matches": False}, status=status.HTTP_200_OK)
        
        return Response({"password_matches": True}, status=status.HTTP_200_OK)


@extend_schema(tags=['Ratings'])
class RateTutorView(APIView):
    """
    Rate tutor
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = RateTutorSerializer
    
    def post(self, request, tutor_id=None):
        """
        Rate tutor
        """
        if not tutor_id:
            return Response({"Error": _("Tutor id is required.")}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            tutor = Tutor.objects.get(id=tutor_id)
            
        except Tutor.DoesNotExist:
            return Response({"Error": _("Tutor not found.")}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        data = request.data
        
        serializer = self.serializer_class(context={'user': user, 'tutor': tutor} ,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, tutor_id):
        """
        Delete rating
        """
        user = request.user
        try:
            tutor_rating = TutorRatings.objects.get(tutor_id=tutor_id)
        except TutorRatings.DoesNotExist:
            return Response({"Error": _("Rating not found.")}, status=status.HTTP_400_BAD_REQUEST)
        
        tutor_rating.delete()
        return Response({"Info": _("Rating deleted.")}, status=status.HTTP_200_OK)
        
        
@extend_schema(tags=['Ratings'])
class RatingsMeView(APIView):
    """
    Get user ratings
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = RatingsMeSerializer
    
    def get(self, request):
        """
        Get user ratings
        """
        user = request.user
        ratings = TutorRatings.objects.filter(student=user)
        serializer = self.serializer_class(ratings, many=True)
        return Response({"ratings": serializer.data}, status=status.HTTP_200_OK)


@extend_schema(tags=['Ratings'])
class BestRatingsView(generics.ListAPIView):
    """
    Get best ratings
    """
    serializer_class = RatingsMeSerializer
    queryset = TutorRatings.objects.all().order_by('-rating')
    filter_backends = [DjangoFilterBackend]
    filterset_class = RatingsFilter
