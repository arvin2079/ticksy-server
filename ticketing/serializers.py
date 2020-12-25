from rest_framework import serializers
from ticketing.models import Topic, ACTIVE
from users.serializers import UserSerializer#, UserSerializerForView
from users.models import User


class TopicSerializer(serializers.ModelSerializer):

    CREATOR   = 'سازنده'
    SUPPORTER = 'ادمین'

    role = serializers.SerializerMethodField()
    #creator = UserSerializerForView()
    #supporters = UserSerializerForView()
    class Meta:
        model  = Topic
        fields = '__all__'
        read_only_fields = ['creator', 'is_active']
        #depth = 1

    def get_role(self, obj):
        if self.context['request'].user == obj.creator:
            return (self.CREATOR)
        return (self.SUPPORTER)

    def create(self, validated_data):
        obj = super().create(validated_data)
        user = self.context['request'].user
        supporters = list(obj.supporters.all())
        if user in supporters:
            supporters.remove(user)
            obj.supporters.set(supporters)
        obj.is_active = ACTIVE
        obj.creator = user
        obj.save()
        return obj
