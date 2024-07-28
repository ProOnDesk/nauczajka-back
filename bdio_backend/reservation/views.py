from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from reservation.serializers import (
    ReservationSerializer,
    ReservationReadOnlySerializer
) 
from reservation.models import TutoringReservation
from reservation.filters import ReservationFilter
from drf_spectacular.utils import extend_schema
from tutor.permissions import IsTutor
from django_filters.rest_framework import DjangoFilterBackend

@extend_schema(tags=['Reservation'])
class ReservationCreateAPIView(APIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Reservation'])
class ReservationTutorMeAPIView(ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, IsTutor]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservationFilter
    
    def get_queryset(self):
        return TutoringReservation.objects.filter(tutor=self.request.user.tutor)
    

    
    
@extend_schema(tags=['Reservation'])
class ReservationUserMeAPIView(ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, IsTutor]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservationFilter

    def get_queryset(self):
        return TutoringReservation.objects.filter(user=self.request.user)
    


@extend_schema(tags=['Reservation'])
class ReservationTutorMeConfirmAPIView(APIView):
    serializer_class = ReservationReadOnlySerializer
    permission_classes = [IsAuthenticated, IsTutor]
    
    def post(self, request, id):
        reservation = TutoringReservation.objects.get(id=id, tutor=request.user.tutor)
        if reservation.is_confirmed:
            return Response({"error": "Reservation is already confirmed"}, status=status.HTTP_400_BAD_REQUEST)
        reservation.is_confirmed = True
        reservation.save()
        serializer = self.serializer_class(reservation)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
