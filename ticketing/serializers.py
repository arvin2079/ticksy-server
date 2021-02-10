from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from ticketing.models import Topic, Ticket, Message, Attachment, ANSWERED, WAITING_FOR_ANSWER
from users.serializers import UserSerializerRestricted
from users.models import User, IDENTIFIED

CREATOR = '1'
SUPPORTER = '2'


class TopicsSerializer(serializers.ModelSerializer):
    supporters_ids = serializers.PrimaryKeyRelatedField(source='supporters', queryset=User.objects.filter(
        Q(identity__status=IDENTIFIED) & (
                Q(identity__expire_time__isnull=True) | Q(identity__expire_time__gt=timezone.now()))),
                                                        write_only=True, many=True)
    role = serializers.SerializerMethodField()
    creator = UserSerializerRestricted(read_only=True)
    supporters = UserSerializerRestricted(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'creator', 'role', 'title', 'description', 'slug', 'url', 'avatar', 'supporters',
                  'supporters_ids']
        read_only_fields = ['id', 'creator', 'role', 'is_active', 'url', 'supporters']
        extra_kwargs = {
            'url': {'view_name': 'topic-retrieve-update-destroy', 'lookup_field': 'slug'}
        }

    def validate_supporters_ids(self, value):
        supporters = value
        user = self.context['request'].user
        if user in supporters:
            supporters.remove(user)
        return supporters

    def get_role(self, obj):
        if self.context['request'].user == obj.creator:
            return CREATOR
        return SUPPORTER

    def create(self, validated_data):
        instance = super().create(validated_data)
        user = self.context['request'].user
        instance.creator = user
        instance.supporters.set([])
        if 'supporters' in validated_data:
            instance.supporters.set(validated_data['supporters'])
        instance.save()
        return instance


class TopicSerializer(TopicsSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'creator', 'role', 'title', 'description', 'url', 'avatar', 'supporters', 'supporters_ids']
        read_only_fields = ['id', 'creator', 'role', 'is_active', 'title', 'supporters', 'url']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'view_name': 'topic-retrieve-update-destroy', 'lookup_field': 'slug'}
        }

    def update(self, instance, validated_data):
        if 'description' in validated_data:
            instance.description = validated_data['description']
        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']
        if 'supporters' in validated_data:
            instance.supporters.set(validated_data['supporters'])
        instance.save()
        return instance


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['attachmentfile']


class TicketSerializer(serializers.ModelSerializer):
    text = serializers.CharField(write_only=True)
    attachments = serializers.ListField(child=serializers.FileField(), write_only=True)
    creator = UserSerializerRestricted(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'creator', 'title', 'status', 'priority', 'text', 'attachments', 'last_update', 'creation_date',
                  'url']
        read_only_fields = ['id', 'creator', 'topic', 'status']
        extra_kwargs = {
            'url': {'view_name': 'message-list-create', 'lookup_field': 'id'}
        }

    def create(self, validated_data):
        user = self.context['request'].user
        text = validated_data['text']
        attachments = validated_data['attachments']
        validated_data.pop('text')
        validated_data.pop('attachments')
        validated_data['creator'] = user
        validated_data['topic'] = Topic.objects.get(slug=self.context.get('view').kwargs.get('slug'))
        instance = super().create(validated_data)
        message = Message.objects.create(user=user, date=timezone.now(), text=text, ticket=instance)
        for attachment in attachments:
            Attachment.objects.create(message=message, attachmentfile=attachment)
        return instance


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializerRestricted(read_only=True)
    attachment_set = AttachmentSerializer(read_only=True, many=True)
    attachments = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)

    class Meta:
        model = Message
        fields = ['id', 'user', 'date', 'rate', 'text', 'url', 'attachment_set', 'attachments']
        read_only_fields = ['id', 'user', 'rate', 'date', 'attachment_set', 'url']
        extra_kwargs = {
            'url': {'view_name': 'message-rate-update', 'lookup_field': 'id'}
        }

    def create(self, validated_data):
        attachments = validated_data.pop('attachments', [])
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['ticket'] = Ticket.objects.get(id=self.context.get('view').kwargs.get('id'))
        instance = super().create(validated_data)
        for attachment in attachments:
            Attachment.objects.create(attachmentfile=attachment, message=instance)
        if instance.user in instance.ticket.topic.supporters.all() or instance.user == instance.ticket.topic.creator:
            instance.ticket.status = ANSWERED
        else:
            instance.ticket.status = WAITING_FOR_ANSWER
        instance.ticket.save()

        return instance


class MessageUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializerRestricted(read_only=True)
    attachment_set = AttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Message
        fields = ['id', 'user', 'date', 'rate', 'text', 'attachment_set']
        read_only_fields = ['id', 'user', 'date', 'text', 'attachment_set']

    def update(self, instance, validated_data):
        if 'rate' in validated_data:
            instance.rate = validated_data['rate']
        instance.save()
        return instance


class RecommendedTopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['title', 'description', 'slug', 'url', 'avatar']
        read_only_fields = fields
        extra_kwargs = {
            'url': {'view_name': 'topic-retrieve-update-destroy', 'lookup_field': 'slug'}
        }
