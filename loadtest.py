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
messages: list = []

class QuickStartUser(HttpUser):
    token: str = ""
    user_id: int = ""
    header: dict = {}

    wait_time = between(0.5, 10)

    def on_start(self):
        with self.client.post('users/api/signin/', data={
            "username": "mahmoodh1378@gmail.com",
            "password": "123"
        }) as response:
            if response.status_code >= 200 and response.status_code < 300:
                self.token = response.json()["token"]
                self.user_id = response.json()["user_id"]
                self.header = {"Authorization": "token " + self.token}
    
    # @task(5)
    # def user_create(self):
    #     print({
    #         "email": f"m{randint(0,100000)}{randint(0,100000)}{randint(0,100000)}{randint(0,100000)}{randint(0,100000)}@gmail.com",
    #         "first_name": "علی",
    #         "last_name": "اکبری",
    #         "password": "fds;kerw,89757_+2@sfdtgD",
    #         "code": randint(1, 9)
    #     })
    #     self.client.post('users/api/signup/', data={
    #         "email": f"m{randint(0,100000)}{randint(0,100000)}{randint(0,100000)}{randint(0,100000)}{randint(0,100000)}@gmail.com",
    #         "first_name": "علی",
    #         "last_name": "اکبری",
    #         "password": "fds;kerw,89757_+2@sfdtgD",
    #         "code": randint(1, 9)
    #     })
    
    @task(5)
    def user_get(self):
        self.client.get('users/api/identity/', headers=self.header)
    
    @task(5)
    def topic_list(self):
        self.client.get("topic/", headers=self.header)
    
    @task(5)
    def topic_create(self):
        global title, num, description, topic_ids
        try:
            with self.client.post("topic/", data={
                "title": title.format(num),
                "description": description.format(num),
                "avatar": None
            }, headers=self.header) as response:
                topic_ids.append(response.json()['id'])
                num += 1
        except:
            pass

    @task(10)
    def topic_retrieve(self):
        global topic_ids
        if len(topic_ids) > 1:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            self.client.get(f"topic/{id}/", headers=self.header, name="/topic/(-id-)/")
    
    @task(1)
    def topic_destroy(self):
        global topic_ids
        if len(topic_ids) >= 20:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            topic_ids.remove(id)
            self.client.delete(f"topic/{id}/", headers=self.header, name="/topic/(-id-)/")
    
    @task(5)
    def topic_update(self):
        global topic_ids, title, description, num
        try:
            if len(topic_ids) > 1:
                id = topic_ids[randint(0, len(topic_ids) - 1)]
                self.client.put(f"topic/{id}/", data={
                "title": title.format(num),
                "description": description.format(num),
                "avatar": None
                }, headers=self.header,
                name="/topic/(-id-)/")
        except:
            pass
    
    @task(5)
    def role_create(self):
        global topic_ids, roles, title, num, admins
        try:
            if len(topic_ids) > 1:
                id = topic_ids[randint(0, len(topic_ids) - 1)]
                with self.client.post(f"topic/{id}/role/", data={
                    "title": title.format(num),
                    "users": []
                }, headers=self.header, name="/topic/(-id-)/role/") as response:
                    if id in admins.keys() and len(admins[id]) > 0:
                        admins[id].append(response.json()['id'])
                    else:
                        admins[id] = [response.json()['id']]
                    if id in roles.keys():
                        roles[id].append(response.json()['id'])
                    else:
                        roles[id] = [response.json()['id']]
        except:
            pass
    
    @task(10)
    def role_list(self):
        global topic_ids
        if len(topic_ids) > 1:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            self.client.get(f"topic/{id}/role/", 
                headers=self.header,
                name="/topic/(-id-)/role/")
    
    @task(10)
    def role_retrieve(self):
        global topic_ids, roles
        if len(topic_ids) > 1:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            if id in roles.keys() and len(roles[id]) > 1:
                roleid = roles[id][randint(0, len(roles[id]) - 1)]
                self.client.get(f"topic/{id}/role/{roleid}/",
                    headers=self.header,
                    name="/topic/(-id-)/role/(-roleid-)/")
    
    # @task(1)
    # def role_destroy(self):
    #     global topic_ids, roles
    #     if len(topic_ids) > 1:
    #         id = topic_ids[randint(0, len(topic_ids) - 1)]
    #         if id in roles.keys() and len(roles[id]) > 1:
    #             roleid = roles[id][randint(0, len(roles[id]) - 1)]
    #             self.client.delete(f"topic/{id}/role/{roleid}/", 
    #                 headers=self.header,
    #                 name="/topic/(-id-)/role/(-roleid-)/")
    #             roles[id].remove(roleid)
    
    @task(5)
    def role_update(self):
        global topic_ids, roles, title, num
        try:
            if len(topic_ids) > 1:
                id = topic_ids[randint(0, len(topic_ids) - 1)]
                if id in roles.keys() and len(roles[id]) > 1:
                    roleid = roles[id][randint(0, len(roles[id]) - 1)]
                    self.client.put(f"topic/{id}/role/{roleid}/", data={
                    "title": title.format(num),
                    "users": []
                }, headers=self.header, name="/topic/(-id-)/role/(-roleid-)/")
        except:
            pass
    
    @task(15)
    def category_create(self):
        global topic_ids, roles, title, description, num, admins, categories
        try:
            if len(topic_ids) > 1:
                id = topic_ids[randint(0, len(topic_ids) - 1)]
                if id in admins.keys() and len(admins[id]) > 1:
                    admin_id = admins[id][randint(0, len(admins[id]) - 1)]
                    with self.client.post(f"topic/{id}/category/", data={
                        "title": title.format(num),
                        "description": description.format(num),
                        "admin": admin_id,
                        "avatar": None
                    }, headers=self.header, name="/topic/(-id-)/category/") as response:
                        if id in categories.keys() and len(categories[id]) > 0:
                            categories[id].append(response.json()['id'])
                        else:
                            categories[id] = [response.json()['id']]
        except:
            pass
    
    @task(10)
    def category_list(self):
        global topic_ids, roles, title, description, num, admins, categories
        if len(topic_ids) > 1:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            self.client.get(f"topic/{id}/category/", 
                headers=self.header,
                name="/topic/(-id-)/category/")
    

    @task(10)
    def topic_list_all_users(self):
        global topic_ids, roles, title, description, num, admins, categories
        if len(topic_ids) > 1:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            self.client.get(f'topic/{id}/get-all-users/', headers=self.header,
                name="/topic/(-id-)/get-all-users/")

    @task(10)
    def category_retrieve(self):
        global topic_ids, roles, title, description, num, admins, categories
        if len(topic_ids) > 1:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            if id in categories.keys() and len(categories[id]) > 1:
                category_id = categories[id][randint(0, len(categories[id]) - 1)]
                self.client.get(f"topic/{id}/category/{category_id}/", 
                    headers=self.header,
                    name="/topic/(-id-)/category/(-category_id-)/")

    @task(1)
    def category_destroy(self):
        global topic_ids, roles, title, description, num, admins, categories
        if len(topic_ids) > 1:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            if id in categories.keys() and len(categories[id]) > 1:
                category_id = categories[id][randint(0, len(categories[id]) - 1)]
                self.client.delete(f"topic/{id}/category/{category_id}/", 
                    headers=self.header,
                    name="/topic/(-id-)/category/(-category_id-)/")
                categories[id].remove(category_id)
    
    @task(5)
    def category_update(self):
        global topic_ids, roles, title, description, num, admins, categories
        try:
            if len(topic_ids) > 1:
                id = topic_ids[randint(0, len(topic_ids) - 1)]
                if id in categories.keys() and len(categories[id]) > 1 and id in admins.keys() and len(admins[id]) > 1:
                    category_id = categories[id][randint(0, len(categories[id]) - 1)]
                    admin_id = admins[id][randint(0, len(admins) - 1)]
                    self.client.put(f"topic/{id}/category/{category_id}/", data={
                        "title": title.format(num),
                        "description": description.format(num),
                        "admin": admin_id,
                        "avatar": None
                    }, headers=self.header, name="/topic/(-id-)/category/(-category_id-)/")
        except:
            pass
    
    @task(10)
    def ticket_create(self):
        global topic_ids, categories, tickets, title, num
        try:
            if len(topic_ids) > 1:
                id = topic_ids[randint(0, len(topic_ids) - 1)]
                if id in categories.keys() and len(categories[id]) > 1:
                    category_id = categories[id][randint(0, len(categories[id]) - 1)]
                    with self.client.post('ticket/', data={
                        "title": title.format(num),
                        "priority": randint(1, 3),
                        "text": title.format(num),
                        "section": category_id,
                        "attachments": [],
                        "tags": ""
                    }, headers=self.header) as response:
                        tickets.append(response.json()['id'])
        except:
            pass
    
    # @task(5)
    # def ticket_update(self):
    #     global topic_ids, categories, tickets, title, num
    #     try:
    #         if len(tickets) > 1:
    #             id = tickets[randint(0, len(tickets) - 1)]
    #             with self.client.patch(f'ticket/{id}/', data={
    #                 "title": title.format(num),
    #                 "priority": randint(1, 3),
    #                 "tags": ""
    #             }, headers=self.header, name='/ticket/(-id-)/') as response:
    #                 tickets.append(response.json()['id'])
    #     except:
    #         pass

    @task(10)
    def ticket_list(self):
        global topic_ids, categories, tickets, title, num
        self.client.get('ticket/?type=1', headers=self.header)
    
    @task(10)
    def ticket_retrieve(self):
        global topic_ids, categories, tickets, title, num
        if len(topic_ids) > 1 and len(tickets) > 1:
            id = topic_ids[randint(0, len(topic_ids) - 1)]
            ticket_id = tickets[randint(0, len(tickets) - 1)]
            self.client.get(f'ticket/{ticket_id}/', 
                headers=self.header, 
                name="/ticket/(-id-)/")


    # @task(1)
    # def ticket_internal_transmission(self):
    #     global topic_ids, categories, tickets, title, num
    #     if len(topic_ids) > 1 and len(tickets) > 1:
    #         id = topic_ids[randint(0, len(topic_ids) - 1)]
    #         if id in admins.keys() and len(admins[id]) > 1:
    #             admin_id = admins[id][randint(0, len(admins[id]) - 1)]
    #             ticket_id = tickets[randint(0, len(tickets) - 1)]
    #             self.client.put(f'ticket/{ticket_id}/internal-transition/', 
    #                 data={'admin': admin_id}, headers=self.header,
    #                 name='/ticket/(-ticket_id-)/internal-transition/')


    @task(5)
    def message_create(self):
        global topic_ids, categories, description, tickets, title, num, messages
        try:
            if len(tickets) > 1:
                ticket_id = tickets[randint(0, len(tickets) - 1)]
                with self.client.post(f'ticket/{ticket_id}/message/', data={
                    "text": description.format(num),
                    "attachments": []
                }, headers=self.header, name="/message/(-id-)/message/") as response:
                    messages.append(response.json()['id'])
        except:
            pass
    
    @task(5)
    def rate(self):
        global topic_ids, categories, description, tickets, title, num, messages
        if len(messages) > 1:
            message_id = messages[randint(0, len(messages) - 1)]
            self.client.patch(f'message/{message_id}/', data={
                "rate": randint(1, 5)
            }, headers=self.header, name="/message/(-id-)/")
    
    @task(10)
    def topics(self):
        self.client.get('all-topics/', headers=self.header)
    
    @task(10)
    def emails(self):
        self.client.get('email/', headers=self.header)
    
    @task(10)
    def get_recommended_topics(self):
        self.client.get('get-recommended-topics/', headers=self.header)