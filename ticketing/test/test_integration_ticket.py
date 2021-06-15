from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.urls import reverse

from ticketing.models import Topic, Admin, Section
from users.models import User, IDENTIFIED

"""
scenarois doc address path: https://docs.google.com/document/d/188OacAZRv_25gqC7y3psLOKbcyyZJTDT/edit#
the document access is private for team members but feel free to request access for this content. 

Testing Scenarios As Integration Test:
TestIntegrationTicket -> the scenario steps which we'll test here are mentioned bellow : 

    1. [users section \ Authentication module] user login and identified so he/she would be able to create topic and 
       have the ability of performing some change and modification on their topic (or the topic that they are set there 
       as Admin user).
       
    2. [ticketing section \ Topic-Admin-Section module] on the second step user decides to create an simple topic with 
       minimum initial data and information then topic creator set one or more admin user for the created topic. after
       that adding one section to the created topic and also setting a admin user for created section of our specific 
       topic with one admin.
    
    3. [ticketing section \ Ticket module] ordinary user create a ticket then send one message through the ticket.
    
    4. [ticketing section \ Ticket module] supporter of the ticket answer to the user message on the mentioned ticket.

"""

class TestIntegrationTicket(TestCase):

    def setUp(self):
        self.ordinary_client = Client()
        self.supporter_client = Client()

    def test_main(self):
        supporter_user = User.objects.create_user(
            email='su@test.com',
            password='sutest',
        )

        supporter_user.identity.status = IDENTIFIED
        supporter_user.identity.save()

        supporter_user.identity.request_time = datetime.now() - timedelta(days=3)
        supporter_user.identity.expire_time = datetime.now() + timedelta(days=10)
        supporter_user.identity.status = IDENTIFIED
        supporter_user.identity.save()

        self.supporter_client.force_login(supporter_user)

        topic = Topic.objects.create(
            creator=supporter_user,
            title='test topic',
            description='this is for test purposes!',
        )

        admin = Admin.objects.create(
            title='admin',
            topic_id=topic.id,
        )
        admin.users.add(supporter_user)
        admin.save()

        section = Section.objects.create(
            topic=topic,
            description='section description',
            admin=admin,
        )

        ordinary_user = User.objects.create_user(
            email='cu@test.com',
            password='cutest',
        )
        self.ordinary_client.force_login(ordinary_user)

        url = reverse('ticket-list-create')

        body = {
            'creator': ordinary_user.id,
            'title': 'ticket topic',
            'priority': '1',
            'section': section.id,
            'text': 'hello!',
        }

        ord_user_response = self.ordinary_client.post(url, body)
        self.assertEqual(ord_user_response.status_code, 201)

        sup_user_response = self.supporter_client.get(url)
        self.assertEqual(sup_user_response.status_code, 200)

        url = reverse('ticket-create', args=[topic.id, ])
        body = {
            "text": "how are you",
        }

        sup_user_response = self.supporter_client.post(url, body)
        self.assertEqual(sup_user_response.status_code, 201)
