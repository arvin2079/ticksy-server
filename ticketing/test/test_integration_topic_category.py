from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.urls import reverse

from ticketing.models import Topic, Admin, Section
from users.models import User, IDENTIFIED

"""
scenarois doc address path: https://docs.google.com/document/d/188OacAZRv_25gqC7y3psLOKbcyyZJTDT/edit#
the document access is private for team members but feel free to request access for this content. 

Testing Scenarios As Integeration Test:
TestIntegrationTicket -> the scenario steps which we'll test here are mainmain bellow : 

    1. [users section \ Authenticaion module] user login and identified so he/she would be able to create topic and 
       have the ability of performing some change and modification on their topic (or the topic that they are set there 
       as Admin user).
       
    2. [ticketing section \ Topic module] on the second step user decides to create an simple topic with minimume 
       initial data and information.
       
    3. [ticketing section \ Admin module] third step is along with previous step. in this step topic creator set one or 
       more admin user for the created topic.
    
    4. [ticketing section \ Section module] adding one section to the created topic.
    
    5. [ticketing section \ Admin module] setting a admin user for created section of our specific topic.
    
    6. [ticketing section \ Topic module] update some of the topic information 
    
    7. [ticketing section \ Section module] update some of the section information 

"""


class TestIntegrationTicket(TestCase):

    def setUp(self):
        self.client = Client()

    def test_main(self):
        topic_creator_user = User.objects.create_user(
            email='tcu@test.com',
            password='tcutest',
        )

        topic_creator_user.first_name = 'آروین'
        topic_creator_user.last_name = 'صادقی'
        topic_creator_user.save()

        topic_creator_user.identity.request_time = datetime.now() - timedelta(days=3)
        topic_creator_user.identity.expire_time = datetime.now() + timedelta(days=10)
        topic_creator_user.identity.status = IDENTIFIED
        topic_creator_user.identity.save()

        self.assertTrue(self.client.login(email='tcu@test.com', password='tcutest'))

        topic_supporters_id = []
        for i in range(3):
            user = User.objects.create_user(
                email='ta' + str(i) + '@test.com',
                password='tatest'
            )

            user.identity.request_time = datetime.now() - timedelta(days=3)
            user.identity.expire_time = datetime.now() + timedelta(days=10)
            user.identity.status = IDENTIFIED
            user.identity.save()

            topic_supporters_id.append(user.id)

        url = reverse('topic-list-create')
        body = {
            "title": "topic one",
            "description": "sample description for topic one",
            "slug": "something",
            "supporters_ids": topic_supporters_id
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)

        topic = Topic.objects.filter(title="topic one").first()

        admin_user = User.objects.get(pk=topic_supporters_id[-1])
        admin = Admin.objects.create(
            title='admin',
            topic=topic,
        )
        admin.users.add(admin_user)
        admin.save()

        url = reverse('section-list-create', args=[topic.id, ])
        body = {
            "title": "section one",
            "description": "description",
            "admin": admin.id
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)

        url = reverse('topic-retrieve-update-destroy', args=[topic.id, ])
        body = {
            "description": "alternate description",
        }

        response = self.client.patch(url, body, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        section = Section.objects.get(title='section one')

        url = reverse('section-retrieve-update-destroy', args=[topic.id, section.id])
        body = {
            "description": "alternate description",
        }

        response = self.client.patch(url, body, content_type='application/json')
        self.assertEqual(response.status_code, 200)
