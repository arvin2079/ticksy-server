from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from users.models import User, Identity, IDENTIFIED, REQUESTED
from ticketing.models import Ticket, Topic
from ticketing.views import TicketListCreateAPIView, TopicListCreateAPIView, \
    TopicRetrieveUpdateDestroyAPIView, TicketListAPIView, MessageListCreateAPIView, \
    TicketRetriveAPIView, MessageUpdateAPIView, EmailListAPIView, \
    GetRecommendedTopicsAPIView

from datetime import datetime, timedelta


class TestUrls(SimpleTestCase):

    def test_topic_list_create_is_resolved(self):
        # url = reverse('ticketing:topic-list-create')
        url = reverse('topic-list-create')
        self.assertEqual(resolve(url).func.view_class, TopicListCreateAPIView)

    def test_topic_retrieve_update_destroy_is_resolved(self):
        url = reverse('topic-retrieve-update-destroy', args=[0, ])
        self.assertEqual(resolve(url).func.view_class, TopicRetrieveUpdateDestroyAPIView)

    def test_ticket_list_create_is_resolved(self):
        url = reverse('ticket-list-create', args=[0, ])
        self.assertEqual(resolve(url).func.view_class, TicketListCreateAPIView)

    def test_ticket_list_is_resolved(self):
        url = reverse('ticket-list')
        self.assertEqual(resolve(url).func.view_class, TicketListAPIView)

    def test_message_list_create_is_resolved(self):
        url = reverse('message-list-create', args=[1, ])
        self.assertEqual(resolve(url).func.view_class, MessageListCreateAPIView)

    def test_ticket_retrive_is_resolved(self):
        url = reverse('ticket-detail', args=[1, ])
        self.assertEqual(resolve(url).func.view_class, TicketRetriveAPIView)

    def test_message_update_is_resolved(self):
        url = reverse('message-rate-update', args=[1, ])
        self.assertEqual(resolve(url).func.view_class, MessageUpdateAPIView)

    def test_EmailListAPIView_is_resolved(self):
        url = reverse('email-list')
        self.assertEqual(resolve(url).func.view_class, EmailListAPIView)

    def test_GetRecommendedTopicsAPIView_is_resolved(self):
        url = reverse('recommended-topics-list')
        self.assertEqual(resolve(url).func.view_class, GetRecommendedTopicsAPIView)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        user = User.objects.create_user(
            email='first@test.com',
            password='testtest',
        )

        user.first_name = 'آروین'
        user.last_name = 'صادقی'
        user.save()


    def test_TopicListCreateAPIView_get(self):
        user = User.objects.first()
        self.client.force_login(user=user)

        user.identity.request_time = datetime.now() - timedelta(days=7)
        user.identity.expire_time = datetime.now() + timedelta(days=7)
        user.identity.save()


        Topic.objects.create(
            creator=user,
            title='test topic',
            description='this is for test purposes!',
        )

        url = reverse('topic-list-create')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        user.identity.status = REQUESTED
        user.identity.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        user.identity.status = IDENTIFIED
        user.identity.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_TopicListCreateAPIView_post(self):
        user = User.objects.first()
        self.client.force_login(user=user)

        user.identity.request_time = datetime.now() - timedelta(days=7)
        user.identity.expire_time = datetime.now() + timedelta(days=7)
        user.identity.save()

        url = reverse('topic-list-create')

        body = {
            "creator": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            },
            "role": "1",
            "title": "عنوان",
            "description": "توضیحات",
            "url": "http://google.com/",
            "supporters": [
                {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email
                },
            ]
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 403)

        user.identity.status = REQUESTED
        user.identity.save()
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 403)

        user.identity.status = IDENTIFIED
        user.identity.save()
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)


    def test_TopicAdminsListCreateAPIView_post(self):
        first_user = User.objects.first()
        self.client.force_login(user=first_user)

        second_user = User.objects.create_user(
            email='second@test.com',
            password='testtes'
        )

        topic = Topic.objects.create(
            creator=first_user,
            title='test topic',
            description='this is for test purposes!',
        )

        url = reverse('topicAdmins-list-create', args=[topic.id, ])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.force_login(second_user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

