from drf_yasg import openapi
from .serializers import *
from users.serializers import UserSerializerRestricted

_403 = openapi.Response(
    description='You are not still authenticated by admins.',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Description of error'
            )
        }
    ),
    examples={
        'application/json': {
            "detail": "هویت شما هنوز توسط ادمین تایید نشده است."
        }
    }
)

_401 = openapi.Response(
    description='You are not logged in.',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Description of error'
            )
        }
    ),
    examples={
        'application/json': {
            "detail": "اطلاعات برای اعتبارسنجی ارسال نشده است."
        }
    }
)

_404 = openapi.Response(
    description='The Topic not found.',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Description of error'
            )
        }
    ),
    examples={
        'application/json': {
            "detail": "یافت نشد."
        }
    }
)

get_email_dictionary_response = {
    200: openapi.Response(
        description='It returns 10(or less) emails matched with the searched text from the database with a little bit more of extra data. (id, first_name, last_name)',
        schema=UserSerializerRestricted,
        examples={
            'application/json':
                [
                    {
                        "id": 1,
                        "first_name": "علی",
                        "last_name": "اسکندری",
                        "email": "m@gmail.com"
                    },
                    {
                        "id": 3,
                        "first_name": "احمد",
                        "last_name": "کمالی",
                        "email": "kamali@gmail.com"
                    }
                ]
        }
    )
}

get_topic_dictionary_response = {
    200: openapi.Response(
        description='Returns a topic.\n\"role\" means role of the loged in guy related to this topic.\n\"role\" can have two values: 1=creator and 2=supporter.',
        schema=TopicSerializer,
        examples={
            'application/json': {
                "creator": {
                    "id": 3,
                    "first_name": "علی",
                    "last_name": "اسکندری",
                    "email": "m@gmail.com"
                },
                "role": "1",
                "title": "آموزش دانشگاه خوارزمی",
                "description": "تاپیک مربوط به آموزش دانشکده",
                "url": "http://127.0.0.1:8000/topics/amoozesh-khu",
                "avatar": None,
                "supporters": [
                    {
                        "id": 1,
                        "first_name": "ممد",
                        "last_name": "کرمی",
                        "email": "mh@gmail.com"
                    },
                    {
                        "id": 2,
                        "first_name": "جعفر",
                        "last_name": "کمالی",
                        "email": "jafar@gmail.com"
                    }
                ]
            }
        }
    ),
    404: _404,
    403: _403,
    401: _401
}

put_topic_dictionary_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'description': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Description of the topic'
        ),
        'avatar': openapi.Schema(
            type=openapi.Schema(
                type=openapi.TYPE_FILE,
                description='An Image for the topic'
            )
        ),
        'supporters_ids':
            openapi.Schema(
                title='supporters id\'s',
                type=openapi.TYPE_ARRAY,
                description='The id\'s of new supporters',
                items=openapi.Schema(
                    type=openapi.TYPE_INTEGER
                )
            )
    }
)

put_topic_dictionary_response = {
    200: openapi.Response(
        description='Updates the topic with new given data. (Only a creator can update a topic - it means \"role\" must be equal to 1)',
        schema=TopicSerializer,
        examples=
        {
            'application/json': {
                "creator": {
                    "id": 1,
                    "first_name": "ممد",
                    "last_name": "کرمی",
                    "email": "mh@gmail.com"
                },
                "role": "1",
                "title": "آموزش دانشگاه خوارزمی",
                "description": "تاپیک مربوط به آموزش دانشکده",
                "url": "http://127.0.0.1:8000/topics/amoozesh-khu",
                "avatar": "http://127.0.0.1:8000/media/topic-avatar/amoozesh.png",
                "supporters": [
                    {
                        "id": 2,
                        "first_name": "جعفر",
                        "last_name": "کمالی",
                        "email": "jafar@gmail.com"
                    }
                ]
            }
        }
    ),
    404: _404,
    403: _403,
    401: _401
}

delete_topic_dictionary_response = {
    204: openapi.Response(
        description='The Topic Has Deleted.',
    ),
    404: _404,
    403: _403,
    401: _401
}

get_topics_dictionary_response = {
    200: openapi.Response(
        description='Returns a list of Topics that a user is creator or supporter of them. (users role are recorded in \"role\" value)',
        schema=TopicsSerializer,
        examples={
            'application/json': {
                "count": 3,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "creator": {
                            "id": 2,
                            "first_name": "جعفر",
                            "last_name": "حیدری",
                            "email": "jafar@gmail.com"
                        },
                        "role": "1",
                        "title": "some new shit",
                        "description": "new new new",
                        "url": "http://127.0.0.1:8000/topics/awerwedffkjytr56rytiuh",
                        "avatar": None,
                        "supporters": [
                            {
                                "id": 1,
                                "first_name": "ممد",
                                "last_name": "حیدری",
                                "email": "m@gmail.com"
                            }
                        ]
                    },
                    {
                        "creator": {
                            "id": 1,
                            "first_name": "ممد",
                            "last_name": "حیدری",
                            "email": "m@gmail.com"
                        },
                        "role": "2",
                        "title": "some shit from mamad",
                        "description": "dsa",
                        "url": "http://127.0.0.1:8000/topics/dsgwertryrthfhfg",
                        "avatar": None,
                        "supporters": [
                            {
                                "id": 2,
                                "first_name": "جعفر",
                                "last_name": "حیدری",
                                "email": "jafar@gmail.com"
                            }
                        ]
                    },
                    {
                        "creator": {
                            "id": 1,
                            "first_name": "ممد",
                            "last_name": "حیدری",
                            "email": "m@gmail.com"
                        },
                        "role": "2",
                        "title": "Some title",
                        "description": "Description for title",
                        "url": "http://127.0.0.1:8000/topics/arfdsrweqrqerqrq-reqr-eqrqr",
                        "avatar": None,
                        "supporters": [
                            {
                                "id": 1,
                                "first_name": "ممد",
                                "last_name": "حیدری",
                                "email": "m@gmail.com"
                            },
                            {
                                "id": 2,
                                "first_name": "جعفر",
                                "last_name": "حیدری",
                                "email": "jafar@gmail.com"
                            }
                        ]
                    }
                ]
            }
        }
    ),
    403: _403,
    401: _401
}

post_topics_dictionary_response = {
    201: openapi.Response(
        description='A new Topic is created.',
        schema=TopicsSerializer,
        examples={
            'application/json': {
                "creator": {
                    "id": 2,
                    "first_name": "جعفر",
                    "last_name": "حیدری",
                    "email": "jafar@gmail.com"
                },
                "role": "1",
                "title": "عنوان",
                "description": "توضیحات",
                "url": "http://127.0.0.1:8000/topics/tag",
                "avatar": None,
                "supporters": [
                    {
                        "id": 1,
                        "first_name": "ممد",
                        "last_name": "حیدری",
                        "email": "m@gmail.com"
                    },
                    {
                        "id": 2,
                        "first_name": "جعفر",
                        "last_name": "حیدری",
                        "email": "jafar@gmail.com"
                    }
                ]
            }
        }
    ),
    403: _403,
    401: _401
}

post_topic_dictionary_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Title of the topic'
        ),
        'description': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Description of the topic'
        ),
        'slug': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Slug of the topic'
        ),
        'avatar': openapi.Schema(
            type=openapi.Schema(
                type=openapi.TYPE_FILE,
                description='An Image for the topic'
            )
        ),
        'supporters_ids':
            openapi.Schema(
                title='supporters id\'s',
                type=openapi.TYPE_ARRAY,
                description='The id\'s of new supporters',
                items=openapi.Schema(
                    type=openapi.TYPE_INTEGER
                )
            )
    }
)

get_ticket_dictionary_response = {
    200: openapi.Response(
        description='Returns a list of tickets in a topic',
        schema=TicketSerializer,
        examples={
            'application/json': {
                "count": 3,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 20,
                        "creator": {
                            "id": 1,
                            "first_name": "احمد",
                            "last_name": "کلامی",
                            "email": "m@gmail.com"
                        },
                        "title": "عنوانی دیگر",
                        "status": "1",
                        "priority": "3"
                    },
                    {
                        "id": 19,
                        "creator": {
                            "id": 1,
                            "first_name": "احمد",
                            "last_name": "کلامی",
                            "email": "m@gmail.com"
                        },
                        "title": "عنوان جدید 2",
                        "status": "2",
                        "priority": "2"
                    },
                    {
                        "id": 18,
                        "creator": {
                            "id": 1,
                            "first_name": "احمد",
                            "last_name": "کلامی",
                            "email": "m@gmail.com"
                        },
                        "title": "عنوان جدید",
                        "status": "1",
                        "priority": "1"
                    }
                ]
            }
        }
    ),
    403: _403,
    401: _401
}

post_ticket_dictionary_response = {
    201: openapi.Response(
        description='Creates a Ticket',
        schema=TicketSerializer,
        examples={
            'application/json': {
                "id": 22,
                "creator": {
                    "id": 1,
                    "first_name": "ممد",
                    "last_name": "حیدری",
                    "email": "m@gmail.com"
                },
                "title": "new title",
                "status": "1",
                "priority": "1"
            }
        }
    ),
    403: _403,
    401: _401
}

post_ticket_dictionary_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Title of the post'
        ),
        'priority': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Priority of the ticket(Has 3 values including \{1, 2, 3\}, 1 is lowest priority and 3 is the most)'
        ),
        'text': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Message of user for describing what the problem is'
        ),
        'attachments': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_FILE
            ),
            description='A list of files attached to the Message'
        )
    }
)

get_message_dictionary_response = {
    200: openapi.Response(
        description='Returns a list of messages in a ticket',
        schema=MessageSerializer,
        examples={
            'application/json': [
                {
                    "id": 20,
                    "user": {
                        "id": 1,
                        "first_name": "ممد",
                        "last_name": "حیدری",
                        "email": "m@gmail.com"
                    },
                    "date": "2021-01-10T12:15:30.439646",
                    "rate": 3,
                    "text": "نوشته جدید",
                    "url": "http://127.0.0.1:8000/topics/message/20/",
                    "attachment_set": []
                },
                {
                    "id": 26,
                    "user": {
                        "id": 1,
                        "first_name": "ممد",
                        "last_name": "حیدری",
                        "email": "m@gmail.com"
                    },
                    "date": "2021-01-10T18:16:55.999540",
                    "rate": 5,
                    "text": "sadwqewqewqeqwe",
                    "url": "http://127.0.0.1:8000/topics/message/26/",
                    "attachment_set": [
                        {
                            "attachmentfile": "http://127.0.0.1:8000/media/files/Emza_Xq6gYW9.png"
                        },
                        {
                            "attachmentfile": "http://127.0.0.1:8000/media/files/Mahmood_3FkFCKG.jpg"
                        }
                    ]
                }
            ]
        }
    ),
    403: _403,
    401: _401
}

post_message_dictionary_response = {
    201: openapi.Response(
        description='Creates a Message',
        schema=MessageSerializer,
        examples={
            'application/json': {
                "id": 26,
                "user": {
                    "id": 1,
                    "first_name": "ممد",
                    "last_name": "حیدری",
                    "email": "m@gmail.com"
                },
                "date": "2021-01-10T18:16:55.999540",
                "rate": 5,
                "text": "sadwqewqewqeqwe",
                "url": "http://127.0.0.1:8000/topics/message/26/",
                "attachment_set": [
                    {
                        "attachmentfile": "http://127.0.0.1:8000/media/files/Emza_Xq6gYW9.png"
                    },
                    {
                        "attachmentfile": "http://127.0.0.1:8000/media/files/Mahmood_3FkFCKG.jpg"
                    }
                ]
            }
        }
    ),
    403: _403,
    401: _401
}

post_message_dictionary_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'text': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Message of user for describing what the problem is'
        ),
        'attachments': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_FILE
            ),
            description='A list of files attached to the Message'
        )
    }
)

patch_ratemessage_dictionary_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'rate': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='Rate of a message that a user gives to the admin or vice versa (rate can be between {1, 2, 3, 4, 5})'
        )
    }
)

patch_ratemessage_dictionary_response = {
    200: openapi.Response(
        description='Rate of the message has updated',
        schema=MessageUpdateSerializer,
        examples={
            "id": 25,
            "user": {
                "id": 1,
                "first_name": "ممد",
                "last_name": "حیدری",
                "email": "m@gmail.com"
            },
            "date": "2021-01-10T17:47:49.089448",
            "rate": "2",
            "text": "new text",
            "attachment_set": []
        }
    ),
    404: _404,
    403: _403,
    401: _401
}
