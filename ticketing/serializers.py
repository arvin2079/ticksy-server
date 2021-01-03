from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.serializers import ValidationError
from ticketing.models import Topic, ACTIVE
from users.serializers import UserSerializerRestricted
from users.models import User, IDENTIFIED
from datetime import timedelta


CREATOR   = '1'
SUPPORTER = '2'

class TopicsSerializer(serializers.ModelSerializer):

    supporters_ids = serializers.PrimaryKeyRelatedField(source='supporters', queryset=User.objects.filter(Q(identity__status=IDENTIFIED) & Q(identity__expire_time__range=[timezone.now(), timezone.now() + timedelta(weeks=48*4)])), write_only=True, many=True)
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
        instance.supporters.set([])
        if 'supporters' in validated_data:
            instance.supporters.set(validated_data['supporters'])
        instance.save()
        return instance

class TopicSerializer(TopicsSerializer):

    class Meta:
        model  = Topic
        fields = ['creator', 'role', 'title', 'description', 'url', 'avatar', 'supporters', 'supporters_ids']
        read_only_fields = ['creator', 'is_active', 'title', 'supporters']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'view_name': 'topic-retrieve-update-destroy', 'lookup_field': 'slug'}
        }
    
    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user
        instance.creator = user
        if 'description' in validated_data:
            instance.description = validated_data['description']
        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']
        if 'supporters' in validated_data:
            instance.supporters.set(validated_data['supporters'])
        instance.save()
        return instance
