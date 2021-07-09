import time
from random import randint
from locust import HttpUser, task, between


title: str = "title {}"
description: str = "description {}"
num: int = 1
topic_ids: list = []
users: list = []
roles: dict = {}
admins: dict = {}
categories: dict = {}
tickets: list = []

class QuickStartUser(HttpUser):
    token: str = ""
    user_id: int = ""
    header: dict = {}

    wait_time = between(5, 10)

    def on_start(self):
        with self.client.post('users/api/signin/', data={
            "username": "mahmoodh1378@gmail.com",
            "password": "123"
        }) as response:
            if response.status_code >= 200 and response.status_code < 300:
                self.token = response.json()["token"]
                self.user_id = response.json()["user_id"]
                self.header = {"Authorization": "token " + self.token}
    
    @task(5)
    def topic_list(self):
        self.client.get("topic/", headers=self.header)
    
    @task(5)
    def topic_create(self):
        global title, num, description, topic_ids
        with self.client.post("topic/", data={
            "title": title.format(num),
            "description": description.format(num),
            "avatar": None
        }, headers=self.header) as response:
            topic_ids.append(response.json()['id'])
            num += 1

    @task(10)
    def topic_retrieve(self):
        global topic_ids
        if len(topic_ids) > 0:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            self.client.get(f"topic/{id}/", headers=self.header)
    
    @task(1)
    def topic_destroy(self):
        global topic_ids
        if len(topic_ids) >= 20:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            topic_ids.remove(id)
            self.client.delete(f"topic/{id}/", headers=self.header)
    
    @task(5)
    def role_create(self):
        global topic_ids, roles, title, num, admins
        if len(topic_ids) >= 0:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            with self.client.post(f"topic/{id}/role/", data={
                "title": title.format(num),
                "users": [1, 2, 3]
            }, headers=self.header) as response:
                if id in admins.keys() and len(admins[id]) > 0:
                    admins[id].append(response.json()['id'])
                else:
                    admins[id] = [response.json()['id']]
                if id in roles.keys():
                    roles[id].append(response.json()['id'])
                else:
                    roles[id] = [response.json()['id']]
    
    @task(10)
    def role_list(self):
        global topic_ids
        if len(topic_ids) >= 0:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            self.client.get(f"topic/{id}/role/", headers=self.header)
    
    @task(10)
    def role_retrieve(self):
        global topic_ids, roles
        if len(topic_ids) >= 0:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            if id in roles.keys() and len(roles[id]) > 0:
                roleid = roles[id][randint(0, len(roles[id]) - 1)]
                self.client.get(f"topic/{id}/role/{roleid}/", headers=self.header)
    
    @task(1)
    def role_destroy(self):
        global topic_ids, roles
        if len(topic_ids) >= 0:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            if id in roles.keys() and len(roles[id]) > 0:
                roleid = roles[id][randint(0, len(roles[id]) - 1)]
                self.client.delete(f"topic/{id}/role/{roleid}/", headers=self.header)
    
    @task(5)
    def category_create(self):
        global topic_ids, roles, title, description, num, admins, categories
        if len(topic_ids) >= 0:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            if id in admins.keys() and len(admins[id]) > 0:
                admin_id = admins[id][randint(0, len(admins) - 1)]
                with self.client.post(f"topic/{id}/category/", data={
                    "title": title.format(num),
                    "description": description.format(num),
                    "admin": admin_id,
                    "avatar": None
                }, headers=self.header) as response:
                    if id in categories and len(categories[id]) > 0:
                        categories[id].append(response.json()['id'])
                    else:
                        categories[id] = [response.json()['id']]
    
    @task(10)
    def category_list(self):
        global topic_ids, roles, title, description, num, admins, categories
        if len(topic_ids) >= 0:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            self.client.get(f"topic/{id}/category/", headers=self.header)
    
    @task(10)
    def category_retrieve(self):
        global topic_ids, roles, title, description, num, admins, categories
        if len(topic_ids) >= 0:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            if id in categories.keys() and len(categories[id]) > 0:
                category_id = categories[id][randint(0, len(categories) - 1)]
                self.client.get(f"topic/{id}/category/{category_id}/", headers=self.header)

    @task(1)
    def category_destroy(self):
        global topic_ids, roles, title, description, num, admins, categories
        if len(topic_ids) >= 0:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            if id in categories.keys() and len(categories[id]) > 0:
                category_id = categories[id][randint(0, len(categories) - 1)]
                self.client.delete(f"topic/{id}/category/{category_id}/", headers=self.header)
    
    @task(5)
    def ticket_create(self):
        global topic_ids, categories, tickets, title, num
        if len(categories) > 0 and len(topic_ids) > 0:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            category_id = categories[id][randint(0, len(categories) - 1)]
            with self.client.post('ticket/', data={
                "title": title.format(num),
                "priority": randint(1, 3),
                "text": title.format(num),
                "section": categories[id][category_id],
                "attachments": [],
                "tags": ""
            }, headers=self.header) as response:
                tickets.append(response.json()['id'])
    
    @task(10)
    def ticket_list(self):
        global topic_ids, categories, tickets, title, num
        if len(categories) > 0 and len(topic_ids) > 0:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            category_id = categories[id][randint(0, len(categories) - 1)]
            self.client.get('ticket/', headers=self.header)
    
    @task(10)
    def ticket_retrieve(self):
        global topic_ids, categories, tickets, title, num
        if len(categories) > 0 and len(topic_ids) > 0 and len(tickets) > 0:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            category_id = categories[id][randint(0, len(categories) - 1)]
            ticket_id = tickets[randint(0, len(tickets) - 1)]
            self.client.get(f'ticket/{ticket_id}/', headers=self.header)

    @task(5)
    def message_create(self):
        global topic_ids, categories, description, tickets, title, num
        if len(tickets) > 0:
            ticket_id = tickets[randint(0, len(tickets) - 1)]
            self.client.post(f'ticket/{ticket_id}/message/', data={
                "text": description.format(num),
                "attachments": []
            }, headers=self.header)
    
    @task(5)
    def rate(self):
        global topic_ids, categories, description, tickets, title, num
        if len(tickets) > 0:
            ticket_id = tickets[randint(0, len(tickets) - 1)]
            self.client.patch(f'message/{ticket_id}/', data={
                "rate": randint(1, 5)
            }, headers=self.header)