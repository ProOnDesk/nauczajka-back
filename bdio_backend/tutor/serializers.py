from .models import Tutor, Skills
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

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
                    raise ValidationError(f"Skill {skill.skill} does not exist.")
                
                skill_instance = Skills.objects.get(skill=skill.skill)
                tutor.skills.add(skill_instance)
            tutor.save()
        return tutor