from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from reservation.serializers import CreateReservationSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Reservation'])
class ReservationCreateAPIView(APIView):
    serializer_class = CreateReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

