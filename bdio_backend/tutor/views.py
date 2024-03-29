from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from tutor.permissions import IsTutor
from tutor.models import Skills

from .serializers import (
    TutorDescriptionSerializer,
    TutorSkillsSerializer,
    SkillsSerializer,
)

# Create your views here.
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


class TutorSkillsView(APIView):
    """
    View and delete tutor skills
    """
    permission_classes = (IsAuthenticated, IsTutor,)
    serializer_class = TutorSkillsSerializer
    
    def put(self, request, *args, **kwargs):
        """
        Update tutor skills
        """
        serializer = self.serializer_class(request.user.tutor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request,  *args, **kwargs):
        """
        Get tutor skills
        """
        serializer = self.serializer_class(request.user.tutor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SkillsListView(APIView):
    serializer = SkillsSerializer
    
    def get(self, request):
        """
        Get all skills
        """
        skills = Skills.objects.all()
        serializer = self.serializer(skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
