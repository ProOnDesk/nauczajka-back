from rest_framework import serializers
from reservation.models import TutoringReservation
from tutor.serializers import TutorScheduleItemsSerializer
from django.utils.translation import gettext as _


class ReservationSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = TutoringReservation
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'tutor': {'read_only': True},
            'is_confirmed': {'read_only': True},
            'created_at': {'read_only': True}
        }
        
    def validate(self, data):
        """
        Check that the user does not already have a reservation for the same schedule item.
        """
        user = self.context['user']
        schedule_item = data['schedule_item']
        
        if TutoringReservation.objects.filter(user=user, schedule_item=schedule_item).exists():
            raise serializers.ValidationError(_("This schedule item is already reserved for this user."))
        
        return data        
            
    def create(self, validated_data):
        """
        Create a tutoring reservation
        """
        
        user = self.context['user']
        tutor = validated_data['schedule_item'].tutor

        if user.is_tutor and user.tutor == tutor:
            raise serializers.ValidationError(_("You cannot make a reservation for yourself"))
        
        tutoring = TutoringReservation.objects.create(user=user, tutor=tutor, **validated_data)
        return tutoring
        
class ReservationReadOnlySerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = TutoringReservation
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'tutor': {'read_only': True},
            'created_at': {'read_only': True},
            'schedule_item': {'read_only': True},
            'is_confirmed': {'read_only': True}
        }
        

