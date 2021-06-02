from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from ticketing.models import Admin, Section, Topic, Ticket, Message, Attachment, ANSWERED, WAITING_FOR_ANSWER
from users.serializers import UserSerializerRestricted
from users.models import User, IDENTIFIED

CREATOR = '1'
ADMIN = '2'


class AdminsFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admin
        fields = ['id', 'title']
        read_only_fields = ['id']


class TopicsSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    creator = UserSerializerRestricted(read_only=True)
    admins = AdminsFieldSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'creator', 'role', 'title', 'description', 'admins', 'url', 'avatar']
        read_only_fields = ['id', 'creator', 'role', 'admins', 'url']
        extra_kwargs = {
            'url': {'view_name': 'topic-retrieve-update-destroy', 'lookup_field': 'id'}
        }

    def get_role(self, obj):
        if self.context['request'].user == obj.creator:
            return CREATOR
        return ADMIN

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.creator = self.context['request'].user
        instance.save()
        return instance


class TopicSerializer(TopicsSerializer):
    class Meta(TopicsSerializer.Meta):
        lookup_field = 'id'


class TopicAdminsSerializer(AdminsFieldSerializer):

    def to_internal_value(self, data):
        self.fields['users'] = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(Q(is_active=True) & (Q(identity__status=IDENTIFIED) | Q(is_superuser=True))), many=True)
        return super().to_internal_value(data)

    def to_representation(self, instance):
        self.fields['users'] = UserSerializerRestricted(many=True)
        return super().to_representation(instance)

    class Meta(AdminsFieldSerializer.Meta):
        fields = ['id', 'title', 'users']

    def create(self, validated_data):
        validated_data['topic'] = Topic.objects.get(id=self.context['id'])
        instance = super().create(validated_data)
        instance.save()
        return instance


class SectionsSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        self.fields['admin'] = serializers.PrimaryKeyRelatedField(queryset=Admin.objects.filter(Q(topic__id=self.context['id'])))
        return super().to_internal_value(data)

    def to_representation(self, instance):
        self.fields['admin'] = AdminsFieldSerializer(read_only=True)
        return super().to_representation(instance)

    class Meta:
        model = Section
        fields = ['id', 'title', 'description', 'admin', 'avatar']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        validated_data['topic'] = Topic.objects.get(id=self.context['id'])
        instance = super().create(validated_data)
        instance.save()
        return instance


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['attachmentfile']


class TicketSerializer(serializers.ModelSerializer):
    text = serializers.CharField(write_only=True)
    attachments = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
    creator = UserSerializerRestricted(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'creator', 'title', 'status', 'priority', 'text', 'attachments', 'last_update', 'creation_date',
                  'url', 'tags']
        read_only_fields = ['id', 'creator', 'topic', 'status']
        extra_kwargs = {
            'url': {'view_name': 'message-list-create', 'lookup_field': 'id'}
        }

    def create(self, validated_data):
        user = self.context['request'].user
        text = validated_data['text']
        attachments = validated_data.pop('attachments', [])
        validated_data.pop('text')
        validated_data['creator'] = user
        validated_data['topic'] = Topic.objects.get(id=self.context.get('view').kwargs.get('id'))
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
        fields = ['title', 'description', 'url', 'avatar']
        read_only_fields = fields
        extra_kwargs = {
            'url': {'view_name': 'topic-retrieve-update-destroy', 'lookup_field': 'id'}
        }
