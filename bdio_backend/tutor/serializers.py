from .models import Tutor, Skills, TutorScheduleItems
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from user.serializers import UserSerializer
from django.utils.translation import gettext as _

class TutorDescriptionSerializer(ModelSerializer):
    """
    Serializer for the tutor description object
    """
    
    
    class Meta:
        model = Tutor
        fields = ('description',)
        
        
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
        fields = ('start_time', 'end_time')


class TutorSerializer(ModelSerializer):
    """
    Serializer for the tutor object
    """
    first_name = SerializerMethodField() 
    last_name = SerializerMethodField() 
    profile_image = SerializerMethodField()

    class Meta:
        model = Tutor 
        fields = ('id', 'first_name', 'last_name', 'profile_image', 'description', 'skills', 'avg_rating')

    def get_first_name(self, obj):
        """
        Method to get user first name
        """
        return obj.user.first_name

    def get_last_name(self, obj):
        """
        Method to get user last name
        """
        return obj.user.last_name
    
    def get_profile_image(self, obj):
        """
        Method to get user profile image
        """
        return obj.user.profile_image.url
    
    
class TutorDetailSerializer(ModelSerializer):
    """
    Serializer for the tutor detail object
    """
    first_name = SerializerMethodField() 
    last_name = SerializerMethodField() 
    profile_image = SerializerMethodField()
    
    tutor_schedule_items = TutorScheduleItemsSerializer(many=True)
    
    class Meta:
        model = Tutor
        fields = ('first_name', 'last_name', 'profile_image', 'description', 'skills', 'avg_rating', 'tutor_schedule_items')
    
    def get_first_name(self, obj):
        """
        Method to get user first name
        """
        return obj.user.first_name

    def get_last_name(self, obj):
        """
        Method to get user last name
        """
        return obj.user.last_name
    
    def get_profile_image(self, obj):
        """
        Method to get user profile image
        """
        return obj.user.profile_image.url
    
    
class TutorMeScheduleItemsSerializer(ModelSerializer):
    """
    Serializer for the tutor schedule items object
    """
    
    
    class Meta:
        model = TutorScheduleItems
        fields = ('id', 'start_time', 'end_time')
        read_only_fields = ('id',)


    def create(self, validated_data):
        """
        Create a tutor schedule item
        """
        tutor = self.context['tutor']
        schedule_item = TutorScheduleItems.objects.create(tutor=tutor, **validated_data)
        return schedule_item