from django.db.models import Q
from django_filters import rest_framework as filters


class TicketFilter(filters.FilterSet):
    status = filters.filters.NumberFilter(method='filter_status', label='وضعیت')
    topic = filters.filters.CharFilter(method='filter_topic', label='بخش')
    type = filters.filters.NumberFilter(method='filter_type', label='نوع')

    def filter_topic(self, queryset, name, value):
        return queryset.filter(Q(section__topic__title__contains=value))

    def filter_status(self, queryset, name, value):
        if value > 4 or value < 0:
            value = 0
        func = self.switcher.get(value, self.filter_none)
        return func(self, queryset)
    
    def filter_type(self, queryset, name, value):
        if value > 2:
            value = 2
        elif value < 0:
            value = 0
        
        if value == 0:
            return queryset
        elif value == 1:
            return queryset.filter(Q(creator=self.request.user))
        elif value == 2:
            return queryset.filter(Q(admin__users__in=[self.request.user]))

    def filter_none(self, queryset):
        return queryset

    def filter_waiting(self, queryset):
        return queryset.filter(Q(status='1'))

    def filter_processing(self, queryset):
        return queryset.filter(Q(status='2'))

    def filter_answered(self, queryset):
        return queryset.filter(Q(status='3'))

    def filter_closed(self, queryset):
        return queryset.filter(Q(status='4'))

    switcher = {
        0: filter_none,
        1: filter_waiting,
        2: filter_processing,
        3: filter_answered,
        4: filter_closed
    }
