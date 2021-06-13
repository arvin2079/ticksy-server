from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from users.models import User, Identity, IDENTIFIED, REQUESTED
from ticketing.models import Ticket, Topic, Section, Admin, Message
from ticketing.views import TicketListCreateAPIView, TopicListCreateAPIView, \
    TopicRetrieveUpdateDestroyAPIView, MessageUpdateAPIView, EmailListAPIView, \
    GetRecommendedTopicsAPIView, TopicAdminsListCreateAPIView, AdminRetrieveUpdateDestroyAPIView, \
    SectionListCreateAPIView, SectionRetrieveUpdateDestroyAPIView, TicketRetrieveUpdateAPIView, MessageCreateAPIView, \
    TopicsListAPIView

from datetime import datetime, timedelta


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
            "admins": [
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

    def test_TopicAdminsListCreateAPIView_get(self):
        first_user = User.objects.first()
        self.client.force_login(user=first_user)

        second_user = User.objects.create_user(
            email='second@test.com',
            password='testtes',
        )
        second_user.first_name = 'امیرعلی'
        second_user.last_name = 'صبوری'
        second_user.save()

        topic = Topic.objects.create(
            creator=first_user,
            title='test topic',
            description='this is for test purposes!',
        )

        url = reverse('topicAdmins-list-create', args=[topic.id, ])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.force_login(second_user)

        # FIXME
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        topic.admins.add(second_user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_TopicAdminsListCreateAPIView_post(self):
        user = User.objects.first()
        self.client.force_login(user=user)

        user.identity.request_time = datetime.now() - timedelta(days=7)
        user.identity.expire_time = datetime.now() + timedelta(days=7)
        user.identity.status = IDENTIFIED
        user.identity.save()

        topic = Topic.objects.create(
            creator=user,
            title='title',
            description='describtion',
        )

        url = reverse('topicAdmins-list-create', args=[topic.pk, ])

        body = {
            "title": "زدشسدز",
            "users": [user.pk]
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)


    def test_AdminRetrieveUpdateDestroyAPIView_get(self):
        ## TODO
        pass


    def test_SectionListCreateAPIView_get(self):
        topic_creator_user = User.objects.first()
        topic_creator_user.identity.request_time = datetime.now() - timedelta(days=7)
        topic_creator_user.identity.expire_time = datetime.now() + timedelta(days=7)
        topic_creator_user.identity.save()

        self.client.force_login(user=topic_creator_user)

        topic = Topic.objects.create(
            creator=topic_creator_user,
            title='test topic',
            description='this is for test purposes!',
        )

        admin = Admin.objects.create(
            title='admin',
            topic=topic,
        )

        admin.users.add(topic_creator_user)
        admin.save()

        Section.objects.create(
            topic=topic,
            description='section description',
            admin=admin,
        )

        url = reverse('section-list-create', args=[topic.id, ])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_SectionListCreateAPIView_post(self):
        user = User.objects.first()
        self.client.force_login(user)

        topic = Topic.objects.create(
            creator=user,
            title='test topic',
            description='this is for test purposes!',
        )

        admin = Admin.objects.create(
            title='admin',
            topic=topic,
        )
        admin.users.add(user)
        admin.save()

        url = reverse('section-list-create', args=[topic.id, ])

        body = {
            "title": "title",
            "description": "description",
            "admin": admin.id
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)


    def test_TicketListCreateAPIView_get(self):
        user = User.objects.first()
        self.client.force_login(user)

        user.identity.request_time = datetime.now() - timedelta(days=7)
        user.identity.expire_time = datetime.now() + timedelta(days=7)
        user.identity.status = IDENTIFIED
        user.identity.save()

        topic = Topic.objects.create(
            creator_id=user.id,
            title='test topic',
            description='this is for test purposes!',
        )

        admin = Admin.objects.create(
            title='admin',
            topic_id=topic.id,
        )
        admin.users.add(user)
        admin.save()

        section = Section.objects.create(
            topic=topic,
            description='section description',
            admin=admin,
        )

        Ticket.objects.create(
            creator=user,
            title='ticket',
            priority='1',
            section=section,
            admin=admin,
        )

        url = reverse('ticket-list-create')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_TicketListCreateAPIView_post(self):
        user = User.objects.first()
        self.client.force_login(user)

        user.identity.request_time = datetime.now() - timedelta(days=7)
        user.identity.expire_time = datetime.now() + timedelta(days=7)
        user.identity.status = IDENTIFIED
        user.identity.save()

        topic = Topic.objects.create(
            creator_id=user.id,
            title='test topic',
            description='this is for test purposes!',
        )

        admin = Admin.objects.create(
            title='admin',
            topic_id=topic.id,
        )
        admin.users.add(user)
        admin.save()

        section = Section.objects.create(
            topic=topic,
            description='section description',
            admin=admin,
        )

        url = reverse('ticket-list-create')

        body = {
            'creator': user.id,
            'title': 'title',
            'priority': '1',
            'section': section.id,
            'text': 'sample test',
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)

    def test_MessageCreateAPIView_post(self):
        user = User.objects.first()
        self.client.force_login(user)

        user.identity.request_time = datetime.now() - timedelta(days=7)
        user.identity.expire_time = datetime.now() + timedelta(days=7)
        user.identity.status = IDENTIFIED
        user.identity.save()

        topic = Topic.objects.create(
            creator_id=user.id,
            title='test topic',
            description='this is for test purposes!',
        )

        admin = Admin.objects.create(
            title='admin',
            topic_id=topic.id,
        )
        admin.users.add(user)
        admin.save()

        section = Section.objects.create(
            topic=topic,
            description='section description',
            admin=admin,
        )

        ticket = Ticket.objects.create(
            creator=user,
            title='ticket',
            priority='1',
            section=section,
            admin=admin,
        )

        message = Message.objects.create(
            user=user,
            ticket=ticket,
            text='message'
        )

        url = reverse('message-rate-update', args=[message.id, ])

        body = {
            "rate": 1
        }

        response = self.client.patch(url, body, content_type='application/json')
        self.assertEqual(response.status_code, 200)
