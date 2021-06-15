from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ticketing.views import TopicListCreateAPIView, TopicRetrieveUpdateDestroyAPIView, TopicAdminsListCreateAPIView, \
    AdminRetrieveUpdateDestroyAPIView, SectionListCreateAPIView, SectionRetrieveUpdateDestroyAPIView, \
    TicketListCreateAPIView, TicketRetrieveUpdateAPIView, MessageCreateAPIView, MessageUpdateAPIView, \
    EmailListAPIView, GetRecommendedTopicsAPIView


class TestUrls(SimpleTestCase):

    def test_topic_list_create_is_resolved(self):
        # url = reverse('ticketing:topic-list-create')
        url = reverse('topic-list-create')
        self.assertEqual(resolve(url).func.view_class, TopicListCreateAPIView)

    def test_topic_retrieve_update_destroy_is_resolved(self):
        url = reverse('topic-retrieve-update-destroy', args=[0, ])
        self.assertEqual(resolve(url).func.view_class, TopicRetrieveUpdateDestroyAPIView)

    def test_topic_admins_list_create_is_resolved(self):
        url = reverse('topicAdmins-list-create', args=[0, ])
        self.assertEqual(resolve(url).func.view_class, TopicAdminsListCreateAPIView)

    def test_admin_retrieve_update_destroy_is_resolved(self):
        url = reverse('role-retrieve-update-destroy', args=[0, 0])
        self.assertEqual(resolve(url).func.view_class, AdminRetrieveUpdateDestroyAPIView)

    def test_section_list_create_is_resolved(self):
        url = reverse('section-list-create', args=[0, ])
        self.assertEqual(resolve(url).func.view_class, SectionListCreateAPIView)

    def test_section_retrieve_update_destroy_is_resolved(self):
        url = reverse('section-retrieve-update-destroy', args=[0, 0])
        self.assertEqual(resolve(url).func.view_class, SectionRetrieveUpdateDestroyAPIView)

    def test_ticket_list_create_is_resolved(self):
        url = reverse('ticket-list-create')
        self.assertEqual(resolve(url).func.view_class, TicketListCreateAPIView)

    def test_ticket_retrieve_update_is_resolved(self):
        url = reverse('ticket-retrieve-update', args=[0, ])
        self.assertEqual(resolve(url).func.view_class, TicketRetrieveUpdateAPIView)

    def test_message_create_is_resolved(self):
        url = reverse('ticket-create', args=[0, ])
        self.assertEqual(resolve(url).func.view_class, MessageCreateAPIView)

    def test_message_update_is_resolved(self):
        url = reverse('message-rate-update', args=[1, ])
        self.assertEqual(resolve(url).func.view_class, MessageUpdateAPIView)

    def test_email_list_is_resolved(self):
        url = reverse('email-list')
        self.assertEqual(resolve(url).func.view_class, EmailListAPIView)

    def test_GetRecommendedTopicsAPIView_is_resolved(self):
        url = reverse('recommended-topics-list')
        self.assertEqual(resolve(url).func.view_class, GetRecommendedTopicsAPIView)