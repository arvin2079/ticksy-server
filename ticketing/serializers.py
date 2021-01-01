from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.serializers import ValidationError
from ticketing.models import Topic, ACTIVE
from users.serializers import UserSerializerRestricted
from users.models import User, IDENTIFIED
from datetime import datetime


CREATOR   = '1'
SUPPORTER = '2'

class TopicsSerializer(serializers.ModelSerializer):

    supporters_ids = serializers.PrimaryKeyRelatedField(source='supporters', queryset=User.objects.all(), write_only=True, many=True)
    role = serializers.SerializerMethodField()
    creator = UserSerializerRestricted(read_only=True)
    supporters = UserSerializerRestricted(many=True, read_only=True)

    class Meta:
        model  = Topic
        fields = ['creator', 'role', 'title', 'description', 'slug', 'url', 'avatar', 'supporters', 'supporters_ids']
        read_only_fields = ['creator', 'is_active', 'url', 'supporters']
        extra_kwargs = {
            'url': {'view_name': 'topic-retrieve-update-destroy', 'lookup_field': 'slug'},
            'slug': {'write_only': True}
        }

    def validate_supporters_ids(self, value):
        supporters = value
        user = self.context['request'].user
        if user in supporters:
            supporters.remove(user)
        for supporter in supporters:
            if (supporter.identity.status != IDENTIFIED or (user.identity.expire_time < datetime.now() if user.identity.expire_time else False) and not user.is_superuser):
                supporters.remove(supporter)
        return supporters

    def get_role(self, obj):
        if self.context['request'].user == obj.creator:
            return (CREATOR)
        return (SUPPORTER)

    def create(self, validated_data):
        instance = super().create(validated_data)
        user = self.context['request'].user
        instance.is_active = ACTIVE
        instance.creator = user
        instance.supporters.set(validated_data['supporters'])
        instance.save()
        return instance

class TopicSerializer(TopicsSerializer):

    class Meta:
        model  = Topic
        fields = ['creator', 'role', 'title', 'description', 'slug', 'url', 'avatar', 'supporters', 'supporters_ids']
        read_only_fields = ['creator', 'is_active', 'title', 'slug', 'supporters']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'view_name': 'topic-retrieve-update-destroy', 'lookup_field': 'slug'}
        }
    
    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user
        instance.creator = user
        if(validated_data['description']):
            instance.description = validated_data['description']
        if(validated_data['avatar']):
            instance.avatar = validated_data['avatar']
        if(validated_data['supporters']):
            instance.supporters.set(validated_data['supporters'])
        instance.save()
        return instance
