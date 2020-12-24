from rest_framework import serializers
from ticketing.models import Topic


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Topic
        # fields = ['id', 'title', 'description', 'slug', 'supporters']
        fields = '__all__'
        # todo: need a field to determine role of user against that topic dynamically.
    
    # def create(self, validated_data):
    #     obj         = super().create(validated_data)
    #     supporters  = obj.supporters
    #     validated_supporters = []
    #     for supporter in supporters.all():
    #         try:
    #             User.objects.get(id=supporter.id)
    #         except:
    #             continue
    #         else:
    #             validated_supporters.append(supporter)
    #     obj.supporters.clear()
    #     obj.supporters.set(validated_supporters)
    #     obj.creator     = self.context['request'].user
    #     obj.save()
    #     return obj
    # todo: rewrite serializer and consider both list and create mode
