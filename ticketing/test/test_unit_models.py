from django.test import TestCase
from users.models import User, IDENTIFIED
from ticketing.models import Ticket, Topic, Section, Admin, Message, TicketHistory

from datetime import datetime, timedelta


class TestModels(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            email='ab@ab.com',
            password='12345678',
        )
        user.identity.request_time = datetime.now() - timedelta(days=7)
        user.identity.expire_time = datetime.now() + timedelta(days=7)
        user.identity.status = IDENTIFIED
        user.identity.save()

        self.user = user

    def test_topic_create_successfuly(self):
        Topic.objects.create(
            creator=self.user,
            title='title',
            description='description',
            is_recommended=True,
        )

        topic = Topic.objects.filter(creator=self.user, title='title').first()

        self.assertTrue(hasattr(topic, 'description'))
        self.assertTrue(hasattr(topic, 'is_recommended'))
        self.assertTrue(hasattr(topic, 'avatar'))
        self.assertTrue(hasattr(topic, 'avatar'))

        self.assertEqual(str(topic), topic.title)

    def test_admin_create_successfuly(self):
        topic = Topic.objects.create(
            creator=self.user,
            title='title',
            description='description',
            is_recommended=True,
        )

        admin = Admin.objects.create(
            title='admin title',
            topic=topic,
        )

        users = []
        for i in range(0, 5):
            users.append(User.objects.create_user(
                email='testuser' + f'{i}' + '@test.com',
                password='testtest'
            ))
            users[-1].identity.status = IDENTIFIED
            users[-1].save()

            admin.users.add(users[-1])

        admin.save()

        admin = Admin.objects.filter(title='admin title').first()

        self.assertTrue(hasattr(admin, 'topic'))
        self.assertTrue(hasattr(admin, 'users'))
        self.assertEqual(len(admin.users.all()), len(users))

    def test_section_created_successfuly(self):
        topic = Topic.objects.create(
            creator=self.user,
            title='title',
            description='description',
            is_recommended=True,
        )

        admin = Admin.objects.create(
            title='admin title',
            topic=topic,
        )

        Section.objects.create(
            topic=topic,
            admin=admin,
            title='section title',
            description='sectiond description',
        )

        section = Section.objects.filter(title='section title').first()

        self.assertTrue(hasattr(section, 'is_active'))
        self.assertTrue(hasattr(section, 'avatar'))
        self.assertEqual(str(section), section.title)

    def test_ticket_created_successfuly(self):
        topic = Topic.objects.create(
            creator=self.user,
            title='title',
            description='description',
            is_recommended=True,
        )

        admin = Admin.objects.create(
            title='admin title',
            topic=topic,
        )

        section = Section.objects.create(
            topic=topic,
            admin=admin,
            title='section title',
            description='sectiond description',
        )

        Ticket.objects.create(
            creator=self.user,
            title='ticket title',
            priority='3',
            section=section,
            admin=admin,
        )

        ticket = Ticket.objects.filter(title='ticket title').first()

        self.assertTrue(hasattr(ticket, 'creation_date'))
        self.assertTrue(hasattr(ticket, 'last_update'))
        self.assertTrue(hasattr(ticket, 'tags'))
        self.assertEqual(ticket.status, '1')
        self.assertEqual(str(ticket), ticket.title)

        TicketHistory.objects.create(
            ticket=ticket,
            admin=admin,
            section=section,
            operator=self.user,
        )

        ticket_history = TicketHistory.objects.filter(ticket=ticket).first()

        self.assertTrue(hasattr(ticket_history, 'date'))
        self.assertTrue(hasattr(ticket_history, 'admin'))
        self.assertTrue(hasattr(ticket_history, 'section'))
        self.assertTrue(hasattr(ticket_history, 'operator'))
        self.assertEqual(str(ticket_history), str(ticket_history.id))

    def test_message_created_successfuly(self):
        topic = Topic.objects.create(
            creator=self.user,
            title='title',
            description='description',
            is_recommended=True,
        )

        admin = Admin.objects.create(
            title='admin title',
            topic=topic,
        )

        section = Section.objects.create(
            topic=topic,
            admin=admin,
            title='section title',
            description='sectiond description',
        )

        ticket = Ticket.objects.create(
            creator=self.user,
            title='ticket title',
            priority='3',
            section=section,
            admin=admin,
        )

        Message.objects.create(
            user=self.user,
            ticket=ticket,
            rate=3,
            text='message text'
        )

        message = Message.objects.filter(user=self.user).first()

        self.assertTrue(hasattr(message, 'date'))
        self.assertTrue(hasattr(message, 'ticket'))
        self.assertTrue(hasattr(message, 'text'))
        self.assertTrue(hasattr(message, 'rate'))
        self.assertEqual(message.rate, 3)
