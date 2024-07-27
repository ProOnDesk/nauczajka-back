from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from reservation.serializers import (
    ReservationSerializer,
    ReservationReadOnlySerializer
) 
from reservation.models import TutoringReservation
from drf_spectacular.utils import extend_schema
from tutor.permissions import IsTutor


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
class ReservationTutorMeAPIView(APIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, IsTutor]
    
    def get(self, request):
        reservations = TutoringReservation.objects.filter(tutor=request.user.tutor)
        serializer = self.serializer_class(reservations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
@extend_schema(tags=['Reservation'])
class ReservationUserMeAPIView(APIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, IsTutor]
    
    def get(self, request):
        reservations = TutoringReservation.objects.filter(user=request.user)
        serializer = self.serializer_class(reservations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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
        
