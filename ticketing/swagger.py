from drf_yasg import openapi


get_email_dictionary_response = {
    200: openapi.Response(
        description='It returns 10(or less) emails matched with the searched text from the database with a little bit more of extra data. (id, first_name, last_name)',
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
        examples={
            'application/json':{
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
    400: openapi.Response(
        description='The Topic not found.',
        examples={
            'application/json':{
                "detail": "یافت نشد."
            }
        }
    ),
    403: openapi.Response(
        description='You are not still authenticated by admin and can not access to any topic.',
        examples={
            'application/json':{
                "detail": "هویت شما هنوز توسط ادمین تایید نشده است."
            }
        }
    ),
    401: openapi.Response(
        description='You are not logged in.',
        examples={
            'application/json':{
                "detail": "اطلاعات برای اعتبارسنجی ارسال نشده است."
            }
        }
    )
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
        examples=
        {
            'application/json':{
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
    400: openapi.Response(
        description='The Topic not found.',
        examples={
            'application/json':{
                "detail": "یافت نشد."
            }
        }
    ),
    403: openapi.Response(
        description='You are not still authenticated and can not access to any topic.',
        examples={
            'application/json':{
                "detail": "هویت شما هنوز توسط ادمین تایید نشده است."
            }
        }
    ),
    401: openapi.Response(
        description='You are not logged in.',
        examples={
            'application/json':{
                "detail": "اطلاعات برای اعتبارسنجی ارسال نشده است."
            }
        }
    )
}

delete_topic_dictionary_response = {
    204: openapi.Response(
        description='The Topic Has Deleted.',
    ),
    400: openapi.Response(
        description='The Topic not found.',
        examples={
            'application/json':{
                "detail": "یافت نشد."
            }
        }
    ),
    403: openapi.Response(
        description='You are not owner of the topic,',
        examples={
            'application/json':{
                'detail': 'شما سازنده این تاپیک نیستید.'
            }
        }
    ),
    401: openapi.Response(
        description='You are not logged in.',
        examples={
            'application/json':{
                "detail": "اطلاعات برای اعتبارسنجی ارسال نشده است."
            }
        }
    )
}

get_topics_dictionary_response = {
    200: openapi.Response(
        description='Returns a list of Topics that a user is creator or supporter of them. (users role are recorded in \"role\" value)',
        examples={
            'application/json':{
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
    403: openapi.Response(
        description='You are not still authenticated and can not access to any topic.',
        examples={
            'application/json':{
                "detail": "هویت شما هنوز توسط ادمین تایید نشده است."
            }
        }
    ),
    401: openapi.Response(
        description='You are not logged in.',
        examples={
            'application/json':{
                "detail": "اطلاعات برای اعتبارسنجی ارسال نشده است."
            }
        }
    )
}

post_topics_dictionary_response = {
    201: openapi.Response(
        description= 'A new Topic is created.',
        examples={
            'application/json':{
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
    403: openapi.Response(
        description='You are not still authenticated and can not access to any topic.',
        examples={
            'application/json':{
                "detail": "هویت شما هنوز توسط ادمین تایید نشده است."
            }
        }
    ),
    401: openapi.Response(
        description='You are not logged in.',
        examples={
            'application/json':{
                "detail": "اطلاعات برای اعتبارسنجی ارسال نشده است."
            }
        }
    )
}

{
  "creator": {},
  "title": "string",
  "description": "string",
  "slug": "string",
  "supporters_ids": [
    0
  ]
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