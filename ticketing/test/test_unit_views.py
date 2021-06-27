from django.test import TestCase, Client
from django.urls import reverse

from users.models import User, IDENTIFIED, REQUESTED
from ticketing.models import Ticket, Topic, Section, Admin, Message

from datetime import datetime, timedelta


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

        second_user = User.objects.create_user(
            email='second@test.com',
            password='testtes',
        )

        second_user.first_name = 'امیرعلی'
        second_user.last_name = 'صبوری'
        second_user.identity.status = IDENTIFIED
        second_user.save()

        topic = Topic.objects.create(
            creator=user,
            title='test topic',
            description='this is for test purposes!',
        )

        Topic.objects.create(
            creator=user,
            title='second topic',
            description='this is for test purposes!',
        )

        admin = Admin.objects.create(
            title='test admin',
            topic=topic,
        )

        section = Section.objects.create(
            title='test section',
            topic=topic,
            description='section description',
            admin=admin,
        )

        Ticket.objects.create(
            creator=user,
            title='test ticket',
            priority='1',
            section=section,
            admin=admin,
        )

    def test_TopicListCreateAPIView_get_401(self):
        url = reverse('topic-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_TopicListCreateAPIView_get_403_UNIDENTIFIED(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user=user)

        url = reverse('topic-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_TopicListCreateAPIView_get_403_REQUESTED(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user=user)

        user.identity.status = REQUESTED
        user.identity.save()

        url = reverse('topic-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_TopicListCreateAPIView_get_200(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user=user)

        user.identity.request_time = datetime.now() - timedelta(days=7)
        user.identity.expire_time = datetime.now() + timedelta(days=7)
        user.identity.save()

        url = reverse('topic-list-create')
        user.identity.status = IDENTIFIED
        user.identity.save()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_TopicListCreateAPIView_post_401(self):
        user = User.objects.get(email='first@test.com')

        url = reverse('topic-list-create')
        body = {
            "title": "topic title",
            "description": "topic description",
            "slug": "something",
            "supporters_ids": [
                user.id
            ]
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 401)

    def test_TopicListCreateAPIView_post_403_UNIDENTIFIED(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user=user)

        url = reverse('topic-list-create')
        body = {
            "title": "topic title",
            "description": "topic description",
            "slug": "something",
            "supporters_ids": [
                user.id
            ]
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 403)

    def test_TopicListCreateAPIView_post_403_REQUESTED(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user=user)

        url = reverse('topic-list-create')
        body = {
            "title": "topic title",
            "description": "topic description",
            "slug": "something",
            "supporters_ids": [
                user.id
            ]
        }

        user.identity.status = REQUESTED
        user.identity.save()
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 403)

    def test_TopicListCreateAPIView_post_201(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user=user)

        user.identity.request_time = datetime.now() - timedelta(days=7)
        user.identity.expire_time = datetime.now() + timedelta(days=7)
        user.identity.save()

        url = reverse('topic-list-create')

        body = {
            "title": "topic title",
            "description": "topic description",
            "slug": "something",
            "supporters_ids": [
                user.id
            ]
        }

        user.identity.status = IDENTIFIED
        user.identity.save()
        response = self.client.post(url, body)

        self.assertEqual(response.status_code, 201)

    def test_TopicAdminsListCreateAPIView_get_401(self):
        topic = Topic.objects.get(title='second topic')

        url = reverse('topicAdmins-list-create', args=[topic.id, ])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_TopicAdminsListCreateAPIView_get_403(self):
        user = User.objects.get(email='second@test.com')
        topic = Topic.objects.get(title='second topic')

        self.client.force_login(user)

        url = reverse('topicAdmins-list-create', args=[topic.id, ])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_TopicAdminsListCreateAPIView_get_200_creator_req(self):
        user = User.objects.get(email='first@test.com')
        user.identity.status = IDENTIFIED
        user.save()

        topic = Topic.objects.get(title='second topic')

        self.client.force_login(user=user)

        url = reverse('topicAdmins-list-create', args=[topic.id, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_TopicAdminsListCreateAPIView_get_200_list_admin_req(self):
        user = User.objects.get(email='second@test.com')
        topic = Topic.objects.get(title='second topic')

        self.client.force_login(user=user)

        admin = Admin.objects.create(
            title='admin',
            topic=topic,
        )

        admin.users.add(user)
        admin.save()

        url = reverse('topicAdmins-list-create', args=[topic.id, ])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_TopicAdminsListCreateAPIView_post_401(self):
        user = User.objects.get(email='first@test.com')

        topic = Topic.objects.get(title='test topic')

        url = reverse('topicAdmins-list-create', args=[topic.pk, ])

        body = {
            "title": "زدشسدز",
            "users": [user.pk]
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 401)

    def test_TopicAdminsListCreateAPIView_post_201(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user=user)

        user.identity.request_time = datetime.now() - timedelta(days=7)
        user.identity.expire_time = datetime.now() + timedelta(days=7)
        user.identity.status = IDENTIFIED
        user.identity.save()

        topic = Topic.objects.get(title='test topic')

        url = reverse('topicAdmins-list-create', args=[topic.pk, ])

        body = {
            "title": "زدشسدز",
            "users": [user.pk]
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)

    def test_SectionListCreateAPIView_get_401(self):
        topic_creator_user = User.objects.get(email='first@test.com')
        topic_creator_user.identity.request_time = datetime.now() - timedelta(days=7)
        topic_creator_user.identity.expire_time = datetime.now() + timedelta(days=7)
        topic_creator_user.identity.save()

        topic = Topic.objects.get(title='test topic')

        admin = Admin.objects.get(title='test admin')
        admin.users.add(topic_creator_user)
        admin.save()

        url = reverse('section-list-create', args=[topic.id, ])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_SectionListCreateAPIView_get_404(self):
        topic_creator_user = User.objects.get(email='first@test.com')
        topic_creator_user.identity.request_time = datetime.now() - timedelta(days=7)
        topic_creator_user.identity.expire_time = datetime.now() + timedelta(days=7)
        topic_creator_user.identity.save()

        self.client.force_login(user=topic_creator_user)

        topic = Topic.objects.get(title='test topic')

        admin = Admin.objects.get(title='test admin')
        admin.users.add(topic_creator_user)
        admin.save()

        url = reverse('section-list-create', args=[topic.id + 20, ])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_SectionListCreateAPIView_get_200(self):
        topic_creator_user = User.objects.get(email='first@test.com')
        topic_creator_user.identity.request_time = datetime.now() - timedelta(days=7)
        topic_creator_user.identity.expire_time = datetime.now() + timedelta(days=7)
        topic_creator_user.identity.save()

        self.client.force_login(user=topic_creator_user)

        topic = Topic.objects.get(title='test topic')

        admin = Admin.objects.get(title='test admin')
        admin.users.add(topic_creator_user)
        admin.save()

        url = reverse('section-list-create', args=[topic.id, ])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_SectionListCreateAPIView_post_401(self):
        user = User.objects.get(email='first@test.com')
        topic = Topic.objects.get(title='test topic')

        admin = Admin.objects.get(topic=topic)
        admin.users.add(user)
        admin.save()

        url = reverse('section-list-create', args=[topic.id, ])
        body = {
            "title": "title",
            "description": "description",
            "admin": admin.id
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 401)

    def test_SectionListCreateAPIView_post_403(self):
        user = User.objects.get(email='second@test.com')
        self.client.force_login(user)

        topic = Topic.objects.get(title='test topic')

        admin = Admin.objects.get(topic=topic)
        admin.users.add(user)
        admin.save()

        url = reverse('section-list-create', args=[topic.id, ])
        body = {
            "title": "title",
            "description": "description",
            "admin": admin.id
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 403)

    def test_SectionListCreateAPIView_post_201(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user)

        topic = Topic.objects.get(title='test topic')

        admin = Admin.objects.get(topic=topic)
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

    def test_TicketListCreateAPIView_get_401(self):
        user = User.objects.get(email='first@test.com')

        user.identity.request_time = datetime.now() - timedelta(days=7)
        user.identity.expire_time = datetime.now() + timedelta(days=7)
        user.identity.status = IDENTIFIED
        user.identity.save()

        Ticket.objects.get(title='test ticket')

        url = reverse('ticket-list-create')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_TicketListCreateAPIView_get_200(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user)

        url = reverse('ticket-list-create')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_TicketListCreateAPIView_post_400(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user)

        section = Section.objects.get(title='test section')

        url = reverse('ticket-list-create')
        body = {
            'title': 'title',
            'priority': '1',
            'section': section.id + 20,
            'text': 'sample test',
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 400)

    def test_TicketListCreateAPIView_post_400_2(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user)

        section = Section.objects.get(title='test section')

        url = reverse('ticket-list-create')
        body = {
            'title': 'title',
            'priority': '6',
            'section': section.id,
            'text': 'sample test',
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 400)

    def test_TicketListCreateAPIView_post_401(self):
        section = Section.objects.get(title='test section')

        url = reverse('ticket-list-create')
        body = {
            'title': 'title',
            'priority': '1',
            'section': section.id,
            'text': 'sample test',
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 401)

    def test_TicketListCreateAPIView_post_201(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user)

        section = Section.objects.get(title='test section')

        url = reverse('ticket-list-create')
        body = {
            'title': 'title',
            'priority': '1',
            'section': section.id,
            'text': 'sample test',
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)

    def test_MessageCreateAPIView_post_400_1(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user)

        user.identity.request_time = datetime.now() - timedelta(days=7)
        user.identity.expire_time = datetime.now() + timedelta(days=7)
        user.identity.status = IDENTIFIED
        user.identity.save()

        ticket = Ticket.objects.get(title='test ticket')
        message = Message.objects.create(
            user=user,
            ticket=ticket,
            text='message'
        )

        url = reverse('message-rate-update', args=[message.id + 10, ])
        body = {
            "rate": 1
        }

        response = self.client.patch(url, body, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_MessageCreateAPIView_post_400_2(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user)

        user.identity.request_time = datetime.now() - timedelta(days=7)
        user.identity.expire_time = datetime.now() + timedelta(days=7)
        user.identity.status = IDENTIFIED
        user.identity.save()

        ticket = Ticket.objects.get(title='test ticket')
        message = Message.objects.create(
            user=user,
            ticket=ticket,
            text='message'
        )

        url = reverse('message-rate-update', args=[message.id, ])
        body = {
            "rate": 10
        }

        response = self.client.patch(url, body, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_MessageCreateAPIView_post_401(self):
        user = User.objects.get(email='first@test.com')

        ticket = Ticket.objects.get(title='test ticket')
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
        self.assertEqual(response.status_code, 401)

    def test_MessageCreateAPIView_post_403(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user)

        ticket = Ticket.objects.get(title='test ticket')
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
        self.assertEqual(response.status_code, 403)

    def test_MessageCreateAPIView_post_201(self):
        user = User.objects.get(email='first@test.com')
        self.client.force_login(user)

        user.identity.request_time = datetime.now() - timedelta(days=7)
        user.identity.expire_time = datetime.now() + timedelta(days=7)
        user.identity.status = IDENTIFIED
        user.identity.save()

        ticket = Ticket.objects.get(title='test ticket')
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

    def test_TopicsListAPIView_post(self):
        user = User.objects.first()
        self.client.force_login(user)

        for i in range(5):
            Topic.objects.create(
                creator_id=user.id,
                title='test topic',
                description='this is for test purposes!',
            )

        url = reverse('all-topics')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
