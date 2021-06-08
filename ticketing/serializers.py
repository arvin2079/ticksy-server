from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from ticketing.models import Admin, IN_PROGRESS, Section, TicketHistory, Topic, Ticket, Message, Attachment, ANSWERED, WAITING_FOR_ANSWER
from users.serializers import UserSerializerRestricted
from users.models import User, IDENTIFIED
from ticketing.exception import BadRequest

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


class SectionSerializer(serializers.ModelSerializer):
    
    def to_internal_value(self, data):
        self.fields['admin'] = serializers.PrimaryKeyRelatedField(queryset=Admin.objects.filter(Q(topic__id=self.context['id'])))
        return super().to_internal_value(data)

    def to_representation(self, instance):
        self.fields['admin'] = TopicAdminsSerializer(read_only=True)
        return super().to_representation(instance)

    class Meta:
        model = Section
        fields = ['id', 'title', 'description', 'admin', 'avatar']
        read_only_fields = ['id']


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['attachmentfile']


class TicketsSerializer(serializers.ModelSerializer):
    text = serializers.CharField(write_only=True, label='متن')
    attachments = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
    creator = UserSerializerRestricted(read_only=True)
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.filter(Q(is_active=True) & Q(topic__is_active=True)), label='زیربخش مربوطه', write_only=True)

    def to_representation(self, instance):
        self.fields['section'] = SectionsSerializer(read_only=True)
        return super().to_representation(instance)

    class Meta:
        model = Ticket
        fields = ['id', 'creator', 'title', 'status', 'priority', 'section', 'text', 'attachments', 'last_update', 'creation_date', 'tags']
        read_only_fields = ['id', 'creator', 'status']

    def create(self, validated_data):
        text = validated_data.pop('text', "")
        attachments = validated_data.pop('attachments', [])
        user = self.context['request'].user
        validated_data['creator'] = user
        validated_data['admin'] = validated_data['section'].admin
        instance = super().create(validated_data)
        message = Message.objects.create(user=user, text=text, ticket=instance)
        for attachment in attachments:
            Attachment.objects.create(message=message, attachmentfile=attachment)
        return instance


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializerRestricted(read_only=True)
    attachments = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
    attachment_set = AttachmentSerializer(read_only=True, many=True)

    def to_internal_value(self, data):
        return super().to_internal_value(data)

    class Meta:
        model = Message
        fields = ['id', 'user', 'date', 'rate', 'text', 'url', 'attachments', 'attachment_set']
        read_only_fields = ['id', 'user', 'rate', 'date', 'url', 'attachment_set']
        extra_kwargs = {
            'url': {'view_name': 'message-rate-update', 'lookup_field': 'id'}
        }

    def create(self, validated_data):
        attachments = validated_data.pop('attachments', [])
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['ticket'] = get_object_or_404(Ticket, id=self.context.get('id'))
        instance = super().create(validated_data)
        if self.context.get('request').user in instance.ticket.admin.users.all():
            instance.ticket.status = ANSWERED
        elif self.context.get('request').user == instance.ticket.creator:
            instance.ticket.status = WAITING_FOR_ANSWER
        instance.ticket.save()
        for attachment in attachments:
            Attachment.objects.create(attachmentfile=attachment, message=instance)
        return instance


class TicketHistorySerializer(serializers.ModelSerializer):
    admin = AdminsFieldSerializer(read_only=True)
    operator = UserSerializerRestricted(read_only=True)

    class Meta:
        model = TicketHistory
        fields = ['id', 'admin', 'operator', 'date']


class TicketSerializer(TicketsSerializer):
    section = SectionSerializer(read_only=True)
    message_set = MessageSerializer(many=True, read_only=True)
    tickethistory_set = TicketHistorySerializer(many=True, read_only=True)
    admin = AdminsFieldSerializer(read_only=True)

    def to_internal_value(self, data):
        self.fields['section'] = serializers.PrimaryKeyRelatedField(queryset=Section.objects.filter(Q(is_active=True)))
        self.fields['admin'] = serializers.PrimaryKeyRelatedField(queryset=Admin.objects.all())
        return super().to_internal_value(data)

    class Meta(TicketsSerializer.Meta):
        fields = ['id', 'title', 'status', 'priority', 'section', 'admin', 'tags', 'message_set', 'tickethistory_set', 'last_update', 'creation_date']
        read_only_fields = ['id', 'message_set']

    def update(self, instance, validated_data):
        if validated_data['admin'] not in validated_data['section'].topic.admins.all():
            raise BadRequest(detail={'message': 'نقش انتخاب شده برای رسیدگی به این تیکت، داخل بخش ارسال شده وجود ندارد'})
        TicketHistory.objects.create(ticket=instance, admin=instance.admin, section=instance.section, operator=self.context.get('request').user)
        instance.title = validated_data['title']
        instance.status = validated_data['status']
        instance.priority = validated_data['priority']
        instance.section = validated_data['section']
        instance.admin = validated_data['admin']
        instance.tags = validated_data['tags']
        instance.save()
        return super().create(validated_data)


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
