from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer


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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ProfileUserView(APIView):
    """
    View and update user profile
    """
    # authentication_classes = (TokenAuthentication,)
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