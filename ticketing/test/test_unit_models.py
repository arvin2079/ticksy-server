from django.test import TestCase
from users.models import User, IDENTIFIED
from ticketing.models import Ticket, Topic, Section, Admin, Message, TicketHistory, \
    WAITING_FOR_ANSWER

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

        topic = Topic.objects.create(
            creator=user,
            title='topic title',
            description='topic description',
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

        TicketHistory.objects.create(
            ticket=ticket,
            admin=admin,
            section=section,
            operator=self.user,
        )

        Message.objects.create(
            user=self.user,
            ticket=ticket,
            rate=3,
            text='message text'
        )


    def test_topic_description(self):
        topic = Topic.objects.get(creator=self.user, title='topic title')
        self.assertTrue(hasattr(topic, 'description'))

    def test_topic_is_recommended(self):
        topic = Topic.objects.get(creator=self.user, title='topic title')
        self.assertTrue(hasattr(topic, 'is_recommended'))

    def test_topic_avatar(self):
        topic = Topic.objects.get(creator=self.user, title='topic title')
        self.assertTrue(hasattr(topic, 'avatar'))

    def test_topic_str(self):
        topic = Topic.objects.get(creator=self.user, title='topic title')
        self.assertEqual(str(topic), topic.title)

    def test_admin_topic(self):
        admin = Admin.objects.get(title='admin title')
        self.assertTrue(hasattr(admin, 'topic'))

    def test_admin_users(self):
        admin = Admin.objects.get(title='admin title')
        self.assertTrue(hasattr(admin, 'users'))

    def test_admin_users_add(self):
        admin = Admin.objects.get(title='admin title')

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

        self.assertEqual(len(admin.users.all()), len(users))

    def test_section_is_active(self):
        section = Section.objects.get(title='section title')
        self.assertTrue(hasattr(section, 'is_active'))

    def test_section_avatar(self):
        section = Section.objects.get(title='section title')
        self.assertTrue(hasattr(section, 'avatar'))

    def test_section_str(self):
        section = Section.objects.get(title='section title')
        self.assertEqual(str(section), section.title)

    def test_ticket_creation_date(self):
        ticket = Ticket.objects.get(title='ticket title')
        self.assertTrue(hasattr(ticket, 'creation_date'))

    def test_ticket_last_update(self):
        ticket = Ticket.objects.get(title='ticket title')
        self.assertTrue(hasattr(ticket, 'last_update'))

    def test_ticket_tags(self):
        ticket = Ticket.objects.get(title='ticket title')
        self.assertTrue(hasattr(ticket, 'tags'))

    def test_ticket_status(self):
        ticket = Ticket.objects.get(title='ticket title')
        self.assertEqual(ticket.status, WAITING_FOR_ANSWER)

    def test_ticket_str(self):
        ticket = Ticket.objects.get(title='ticket title')
        self.assertEqual(str(ticket), ticket.title)

    def test_ticket_history_creation_date(self):
        ticket = Ticket.objects.get(title='ticket title')
        ticket_history = TicketHistory.objects.get(ticket=ticket)
        self.assertTrue(hasattr(ticket_history, 'date'))

    def test_ticket_history_admin(self):
        ticket = Ticket.objects.get(title='ticket title')
        ticket_history = TicketHistory.objects.get(ticket=ticket)
        self.assertTrue(hasattr(ticket_history, 'admin'))

    def test_ticket_history_section(self):
        ticket = Ticket.objects.get(title='ticket title')
        ticket_history = TicketHistory.objects.get(ticket=ticket)
        self.assertTrue(hasattr(ticket_history, 'section'))

    def test_ticket_history_operator(self):
        ticket = Ticket.objects.get(title='ticket title')
        ticket_history = TicketHistory.objects.get(ticket=ticket)
        self.assertTrue(hasattr(ticket_history, 'operator'))

    def test_ticket_history_str(self):
        ticket = Ticket.objects.get(title='ticket title')
        ticket_history = TicketHistory.objects.get(ticket=ticket)
        self.assertEqual(str(ticket_history), str(ticket_history.id))

    def test_message_date(self):
        message = Message.objects.get(user=self.user)
        self.assertTrue(hasattr(message, 'date'))

    def test_message_ticket(self):
        message = Message.objects.get(user=self.user)
        self.assertTrue(hasattr(message, 'ticket'))

    def test_message_text(self):
        message = Message.objects.get(user=self.user)
        self.assertTrue(hasattr(message, 'text'))

    def test_message_rate(self):
        message = Message.objects.get(user=self.user)
        self.assertTrue(hasattr(message, 'rate'))

    def test_message_str(self):
        message = Message.objects.get(user=self.user)
        self.assertEqual(message.rate, 3)
