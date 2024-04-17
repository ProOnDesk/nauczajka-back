from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from django.utils.translation import gettext as _

from tutor.permissions import IsTutor
from tutor.models import Skills, Tutor, TutorScheduleItems

from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from .filters import TutorFilter

from .serializers import (
    TutorDescriptionSerializer,
    TutorPriceSerializer,
    TutorSkillsSerializer,
    SkillsSerializer,
    TutorSerializer,
    TutorDetailSerializer,
    TutorMeScheduleItemsSerializer,
    TutorMethodSessionAvailabilitySerializer,
)


@extend_schema(tags=['Tutor Description'])
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


@extend_schema(tags=['Tutor Price'])
class TutorPriceView(APIView):
    """
    View and update tutor description
    """
    permission_classes = (IsAuthenticated, IsTutor,)
    serializer_class = TutorPriceSerializer
    
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


@extend_schema(tags=['Tutor Skills'])
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
        if not request.data.get('skills'):
            tutor = Tutor.objects.get(user=request.user).skills.clear()
            return Response({"skills": []}, status=status.HTTP_200_OK)
        
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
    
@extend_schema(tags=['Tutor Skills'])
class SkillsListView(APIView):
    authentication_classes = []
    serializer_class = SkillsSerializer
    
    def get(self, request):
        """
        Get all skills
        """
        skills = Skills.objects.all()
        serializer = self.serializer_class(skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Tutor all'])
class TutorListView(generics.ListAPIView):
    """
    Get all tutors
    """
    authentication_classes = []
    serializer_class = TutorSerializer
    queryset = Tutor.objects.all()
    permission_classes = (AllowAny,)
    authentication_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_class = TutorFilter
    
    

@extend_schema(tags=['Tutor all'])
class TutorViewSet(viewsets.ViewSet):
    authentication_classes = []
    serializer_class = TutorSerializer
    queryset = Tutor.objects.all()
    
    def list(self, request):
        """
        Get all tutors
        """
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Tutor all'])
class TutorDetailView(generics.RetrieveAPIView):
    """
    Get tutor by id
    """
    authentication_classes = []
    serializer_class = TutorDetailSerializer
    queryset = Tutor.objects.all()
    lookup_field = 'id'
    permission_classes = (AllowAny,)
    

@extend_schema(tags=['Tutor Schedule'])
class RetrieveCreateTutorMeScheduleItemsView(APIView):
    """
    Get tutor schedule items
    """
    permission_classes = (IsAuthenticated, IsTutor,)
    serializer_class = TutorMeScheduleItemsSerializer
    
    def get(self, request):
        """
        Get tutor schedule items
        """
        tutor = request.user.tutor
        schedule_items = tutor.tutor_schedule_items.all()
        serializer = self.serializer_class(schedule_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Create tutor schedule item
        """
        serializer = self.serializer_class(data=request.data, context={'tutor': request.user.tutor})  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if 'non_field_errors' in serializer.errors:
                return Response({"Error": serializer.errors['non_field_errors'][0]}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        """
        Delete all tutor schedule items
        """
        schedule_items = request.user.tutor.tutor_schedule_items.all()
        if not schedule_items:
            return Response({"Info": _("No schedule items found.")}, status=status.HTTP_404_NOT_FOUND)
        
        schedule_items.delete()
        return Response({"Info": _("All schedule items deleted successfully.")}, status=status.HTTP_200_OK)


@extend_schema(tags=['Tutor Schedule'])
class DeleteTutorMeScheduleItemView(APIView):
    """
    Delete tutor schedule item
    """
    permission_classes = (IsAuthenticated, IsTutor,)
    serializer_class = TutorMeScheduleItemsSerializer
    
    def delete(self, request, id):
        """
        Delete tutor schedule item
        """
        try:
            schedule_item = TutorScheduleItems.objects.get(id=id)
        except TutorScheduleItems.DoesNotExist:
            return Response({"Error": _("Schedule item not found.")}, status=status.HTTP_404_NOT_FOUND)
        
        schedule_item.delete()
        
        return Response({"Info": _("Schedule item deleted successfully.")}, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Tutor method session availability'])
class TutorMethodSessionAvailabilityView(APIView):
    """
    View and update tutor method session availability
    """
    permission_classes = (IsAuthenticated, IsTutor,)
    serializer_class = TutorMethodSessionAvailabilitySerializer
    
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
    
@extend_schema(tags=['Tutor Me'])
class TutorMeView(APIView):
    """
    Get my tutor details
    """
    permission_classes = (IsAuthenticated, IsTutor,)
    serializer_class = TutorDetailSerializer
    
    def get(self, request):
        """
        Get my tutor details
        """
        tutor = request.user.tutor
        serializer = self.serializer_class(tutor)
        return Response(serializer.data, status=status.HTTP_200_OK)
