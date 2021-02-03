from django.db.models import F, Q
from django_filters import rest_framework as filters
from .models import Ticket


class TicketFilter(filters.FilterSet):

    status = filters.NumberFilter(method='filter_status', label='وضعیت')

    def filter_status(self, queryset, name, value):
        if value > 4 or value < 0:
            value = 0
        func = self.switcher.get(value, self.filter_none)
        return func(self, queryset)

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
    
    switcher={
        0: filter_none,
        1: filter_waiting,
        2: filter_processing,
        3: filter_answered,
        4: filter_closed
    }
