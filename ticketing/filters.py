from django.db.models import Q
from django_filters import rest_framework as filters

from ticketing.models import Ticket


class TicketFilter(filters.FilterSet):
    TYPE_CHOICES = (
        (1, 'Users'),
        (2, 'Admin'),
    )
    type = filters.filters.ChoiceFilter(choices=TYPE_CHOICES, method='filter_type', help_text='1:users, 2:admins',
                                        required=True)

    class Meta:
        model = Ticket
        fields = ['status', 'section__topic', 'section']

    def filter_type(self, queryset, name, value):
        if value == 1:
            return queryset.filter(Q(creator=self.request.user))
        return queryset.filter(Q(admin__users__in=[self.request.user]))
