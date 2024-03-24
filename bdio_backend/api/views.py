# from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from user.models import User
from rest_framework.response import Response
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    def get_user(self):
        return User.objects.get(email=self.request.data['email'])
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.get_user()
        
        user_is_confirmed = user.is_confirmed
        if not user_is_confirmed:
            return Response({"error": "User is not confirmed"}, status=status.HTTP_400_BAD_REQUEST)

        return response