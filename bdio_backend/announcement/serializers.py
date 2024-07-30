from rest_framework import serializers
from announcement.models import Announcement, Tag
from tutor.models import Tutor
from drf_spectacular.utils import extend_schema_field

class TutorAnnouncementSerializer(serializers.ModelSerializer):

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
            print(request)
            if request is not None:
                return request.build_absolute_uri(obj.user.profile_image.url)
        return None


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

    def to_internal_value(self, data):
        tag_name = data.get('name')
        if not tag_name:
            raise serializers.ValidationError({"name": "This field is required."})
        try:
            tag = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            tag = Tag(name=tag_name)
            tag.save()
        
        return {'name': tag.name, 'tag_instance': tag}

    def create(self, validated_data):
        tag_instance = validated_data.pop('tag_instance', None)
        if tag_instance:
            return tag_instance
        return Tag.objects.create(**validated_data)

class AnnouncementSerializer(serializers.ModelSerializer):
    tutor = TutorAnnouncementSerializer(read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Announcement
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'tutor': {'read_only': True},
            'created_at': {'read_only': True}
        }
        
    def create(self, validated_data):
        tutor = self.context['request'].user.tutor
        tags_data = validated_data.pop('tags')
        
        if len(tags_data) > 50:
            raise serializers.ValidationError({"tags": "Limit of tags is 50"})
        
        announcement = Announcement.objects.create(tutor=tutor, **validated_data)
        
        for tag_data in tags_data:
            print(tag_data)
            announcement.tags.add(tag_data['tag_instance'])
        
        return announcement