from .models import Tutor, Skills, TutorScheduleItems, TutorRatings
from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
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
    first_name = CharField(source='user.first_name') 
    last_name = CharField(source='user.last_name') 
    profile_image = CharField(source='user.profile_image.url')

    class Meta:
        model = Tutor 
        fields = ('id', 'first_name', 'last_name', 'profile_image', 'description', 'skills', 'avg_rating')


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
    profile_image = CharField(source='user.profile_image.url')
    
    tutor_schedule_items = TutorScheduleItemsSerializer(many=True)
    tutor_ratings = RatingsSerializer(many=True)

    
    class Meta:
        model = Tutor
        fields = ('first_name', 'last_name', 'profile_image', 'description', 'skills', 'avg_rating', 'tutor_ratings', 'tutor_schedule_items', )
    
    
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