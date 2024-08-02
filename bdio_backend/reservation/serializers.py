from rest_framework import serializers
from reservation.models import TutoringReservation
from tutor.serializers import TutorScheduleItemsSerializer
from django.utils.translation import gettext as _
from tutor.serializers import TutorMeScheduleItemsSerializer
from tutor.models import Tutor
from user.models import User
from drf_spectacular.utils import extend_schema_field

class UserSerializer(serializers.ModelSerializer):
    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_profile_image(self, obj):
        if hasattr(obj, 'oauth2_picture') and obj.oauth2_picture.view_picture and obj.oauth2_picture.picture_url != "":
            return obj.oauth2_picture.picture_url
        
        if obj.profile_image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.profile_image.url)

        return None
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'id', 'profile_image')
        
        
class TutorSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(source='user.first_name') 
    last_name = serializers.CharField(source='user.last_name') 
    profile_image = serializers.SerializerMethodField()


    class Meta:
        model = Tutor 
        fields = (
            'id', 'first_name', 'last_name', 'profile_image'
        )

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_profile_image(self, obj):
        if obj.user.profile_image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.user.profile_image.url)
            
        return None
        
        
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
        

class TutorReservationSerializer(serializers.ModelSerializer):

    schedule_item = TutorMeScheduleItemsSerializer()
    user = UserSerializer()
    
    
    class Meta:
        model = TutoringReservation
        fields = '__all__'


class UserReservationSerializer(serializers.ModelSerializer):

    schedule_item = TutorMeScheduleItemsSerializer()
    tutor = TutorSerializer()
    
    class Meta:
        model = TutoringReservation
        fields = '__all__'
