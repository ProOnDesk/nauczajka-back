from .models import Tutor, Skills, TutorScheduleItems, TutorRatings
from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from user.serializers import UserSerializer
from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema_field


class SkillsSerializer(ModelSerializer):
    """
    Serializer for the skills object
    """
    
    
    class Meta:
        model = Skills
        fields = ('skill',) 
        
        
class TutorSkillsSerializer(ModelSerializer):
    """
    Serializer for the tutor skills object
    """

    class Meta:
        model = Tutor
        fields = ('skills',)
        
    
    def update(self, instance, validated_data):
        """
        Update the tutor skills
        """
        skills = validated_data.pop('skills', None)
        
        tutor = super().update(instance, validated_data)
        tutor.skills.clear()
        
        if skills:
            for skill in skills:
                if not Skills.objects.filter(skill=skill.skill).exists():
                    raise ValidationError(_(f"Skill {skill.skill} does not exist."))
                
                skill_instance = Skills.objects.get(skill=skill.skill)
                tutor.skills.add(skill_instance)
            tutor.save()
        return tutor


class TutorScheduleItemsSerializer(ModelSerializer):
    """
    Serializer for the tutor schedule items object
    """
    class Meta:
        model = TutorScheduleItems
        fields = ('id', 'start_time', 'end_time', 'is_reserved')


class TutorSerializer(ModelSerializer):
    """
    Serializer for the tutor object
    """
    first_name = CharField(source='user.first_name') 
    last_name = CharField(source='user.last_name') 
    profile_image = SerializerMethodField()


    class Meta:
        model = Tutor 
        fields = (
            'id', 'first_name', 'last_name', 'description', 'price', 'avg_rating', 
            'skills', 'online_sessions_available', 'in_person_sessions_available', 
            'tutoring_location', 'individual_sessions_available', 'group_sessions_available', 
            'profile_image'
        )
        
    @extend_schema_field(CharField(allow_null=True))
    def get_profile_image(self, obj):
        if obj.user.profile_image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.user.profile_image.url)
        return None


class RatingsSerializer(ModelSerializer):
    
    student_first_name = CharField(source='student.first_name')
    student_last_name = CharField(source='student.last_name')
    
    class Meta:
        model = TutorRatings
        fields = ('rating', 'review', 'created_at', 'student_first_name', 'student_last_name')
    
         
class TutorDetailSerializer(ModelSerializer):
    """
    Serializer for the tutor detail object
    """
    first_name = CharField(source='user.first_name') 
    last_name = CharField(source='user.last_name') 
    profile_image = SerializerMethodField()
    user_id = CharField(source='user.id', read_only=True)
    
    tutor_schedule_items = TutorScheduleItemsSerializer(many=True, read_only=True)

    
    class Meta:
        model = Tutor
        fields = ('user_id', 'first_name', 'last_name', 'profile_image', 'description', 'skills', 'avg_rating', 'price',  'tutor_schedule_items', 'online_sessions_available', 'in_person_sessions_available', 'tutoring_location', 'online_sessions_available', 'in_person_sessions_available', 'individual_sessions_available', 'group_sessions_available')
        extra_kwargs = {
            'user_id': {'read_only': True},
            'profile_image': {'read_only': True},
            'avg_rating': {'read_only': True},
            'tutor_schedule_items': {'read_only': True},
        }
        
    @extend_schema_field(CharField(allow_null=True))
    def get_profile_image(self, obj):
        if obj.user.profile_image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.user.profile_image.url)
        return None
    
    
class TutorMeScheduleItemsSerializer(ModelSerializer):
    """
    Serializer for the tutor schedule items object
    """
    
    
    class Meta:
        model = TutorScheduleItems
        fields = ('id', 'start_time', 'end_time', 'is_reserved')
        read_only_fields = ('id',)

    def validate(self, data):
        """
        Validate the schedule item
        """
        try: 
            tutor = self.context['tutor']
            schedule_item = TutorScheduleItems(tutor=tutor, **data)
            schedule_item.clean()
        except ValidationError as e:
            raise ValidationError(_(e.message))
        
        return data
    
    def create(self, validated_data):
        """
        Create a tutor schedule item
        """
        tutor = self.context['tutor']
        schedule_item = TutorScheduleItems.objects.create(tutor=tutor, **validated_data)
        schedule_item.clean()
        return schedule_item
    
    
class TutorMeSerializer(ModelSerializer):
    class Meta:
        model = Tutor
        fields = ('description', 'price', 'online_sessions_available', 'in_person_sessions_available', 'tutoring_location', 'individual_sessions_available', 'group_sessions_available')
        
    def validate_price(self, value):
        """
        Validate the price field
        """
        if value < 0:
            raise ValidationError(_("Price cannot be negative."))
        elif value > 1000000:
            raise ValidationError(_("Price cannot be more than 1000000"))
        return value
        
    def update(self, instance, validated_data):
        """
        Update the tutor object
        """
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.online_sessions_available = validated_data.get('online_sessions_available', instance.online_sessions_available)
        instance.in_person_sessions_available = validated_data.get('in_person_sessions_available', instance.in_person_sessions_available)
        instance.tutoring_location = validated_data.get('tutoring_location', instance.tutoring_location)
        instance.individual_sessions_available = validated_data.get('individual_sessions_available', instance.individual_sessions_available)
        instance.group_sessions_available = validated_data.get('group_sessions_available', instance.group_sessions_available)
        instance.save()
        return instance
