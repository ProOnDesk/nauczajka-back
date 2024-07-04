# from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from user.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
import urllib.parse

from djoser.social.views import ProviderAuthView
from django.conf import settings


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain JWT token pairs (access and refresh tokens).
    This view extends the default TokenObtainPairView from Simple JWT.

    - It verifies user credentials.
    - Checks if the user is confirmed.
    - Sets access and refresh tokens in the response cookies.

    Methods:
    - get_user: Retrieves the user object based on the provided email.
    - post: Handles POST requests to obtain token pairs, and sets cookies.
    """

    def get_user(self):
        """
        Retrieve the user object based on the email provided in the request data.

        Returns:
        User: The user object corresponding to the email.
        """
        return User.objects.get(email=self.request.data['email'])
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to obtain JWT token pairs. 
        Sets the access and refresh tokens in the response cookies if the user is confirmed.

        Parameters:
        request (Request): The HTTP request object.

        Returns:
        Response: HTTP response with JWT tokens or an error message.
        """
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = self.get_user()
            
            user_is_confirmed = user.is_confirmed
            if not user_is_confirmed:
                return Response({"error": "User is not confirmed"}, status=status.HTTP_400_BAD_REQUEST)

            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
        return response


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view to refresh JWT access tokens.
    This view extends the default TokenRefreshView from Simple JWT.

    - It reads the refresh token from cookies.
    - Sets a new access token in the response cookies.

    Methods:
    - post: Handles POST requests to refresh the access token, and sets cookies.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to refresh JWT access token.
        Reads the refresh token from cookies and sets the new access token in the response cookies.

        Parameters:
        request (Request): The HTTP request object.

        Returns:
        Response: HTTP response with new access token or an error message.
        """
        refresh_token = request.COOKIES.get('refresh')
        
        if refresh_token:
            request.data['refresh'] = refresh_token
            
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            
        return response


class CustomTokenVerifyView(TokenVerifyView):
    """
    Custom view to verify JWT access tokens.
    This view extends the default TokenVerifyView from Simple JWT.

    - It reads the access token from cookies.

    Methods:
    - post: Handles POST requests to verify the access token.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to verify JWT access token.
        Reads the access token from cookies and verifies it.

        Parameters:
        request (Request): The HTTP request object.

        Returns:
        Response: HTTP response indicating the token verification result.
        """
        access_token = request.COOKIES.get('access')
       
        if access_token:
            request.data['token'] = access_token
        
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        
        return response
    
    
@extend_schema(
    tags=['OAuth2'],
    parameters=[
        OpenApiParameter(
            name='provider',
            location=OpenApiParameter.PATH,
            description='The authentication provider (e.g., google, facebook).',
            required=True,
            type=str,
            examples=[
                OpenApiExample(
                    'Example 1',
                    value='google-oauth2',
                    description='Google authentication provider'
                ),
                OpenApiExample(
                    'Example 2',
                    value='facebook-oauth2',
                    description='Facebook authentication provider'
                )
            ]
        ),
    ],
)

class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 201:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
        
        return response
