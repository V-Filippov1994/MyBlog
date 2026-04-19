from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from blog_posts.api.serializers import BlogPostSerializer, CommentSerializer


blog_post_docs = dict(
    list=extend_schema(
        summary='Список постов',
        description='Получить список всех постов с возможностью фильтрации и сортировки',
        parameters=[
            OpenApiParameter(name='author__username', description='Фильтр по автору', type=str, required=False),
            OpenApiParameter(name='created_at', description='Фильтр по (YYYY-MM-DD)', type=str, required=False),
            OpenApiParameter(name='created_at_gte', description='Фильтр по дате "от" (YYYY-MM-DD)', type=str, required=False),
            OpenApiParameter(name='created_at_lte', description='Фильтр по дате "до" (YYYY-MM-DD)', type=str, required=False),
            OpenApiParameter(
                name='ordering',
                description='Сортировка: created_at, -created_at, title, -title, likes_count, -likes_count, comments_count, -comments_count',
                type=str,
                required=False
            ),
        ],
        tags=['Posts'],
        examples=[
            OpenApiExample(
                'Успешный ответ',
                value=[
                    {
                        'id': '550e8400-e29b-41d4-a716-446655440000',
                        'title': 'Мой пост',
                        'text': 'Текст',
                        'author': 'User',
                        'created_at': '2026-04-19T12:00:00Z',
                        'updated_at': '2026-04-19T12:00:00Z',
                        'likes_count': 0,
                        'comments_count': 0
                    },
                ],
                response_only=True,
                status_codes=['200']
            ),
        ]
    ),
    create=extend_schema(
        summary='Создать пост',
        description='Создать пост',
        request=BlogPostSerializer,
        tags=['Posts'],
        examples=[
            OpenApiExample(
                'Пример запроса',
                value={
                    'title': 'Новый пост',
                    'text': 'Содержание нового поста'
                },
                request_only=True
            ),
            OpenApiExample(
                'Пример ответа',
                value={
                    'id': 'b86a48e5-8f77-467f-a24c-f3ccbddb095c',
                    'title': 'Новый пост',
                    'text': 'Содержание нового поста',
                    'author': 'User',
                    'created_at': '2026-04-19T00:56:11.430446Z',
                    'updated_at': '2026-04-19T02:19:51.289700Z',
                    'likes_count': 0,
                    'comments_count': 1
                },
                response_only=True,
                status_codes=['201']
            )
        ]
    ),
    retrieve=extend_schema(
        summary='Получить пост',
        description='Получить информацию о посте',
        tags=['Posts'],
        examples=[
            OpenApiExample(
                'Успешный ответ',
                value={
                    'id': '550e8400-e29b-41d4-a716-446655440000',
                    'title': 'Мой пост',
                    'text': 'Содержание поста',
                    'author': 'User',
                    'created_at': '2026-04-19T12:00:00Z',
                    'updated_at': '2026-04-19T12:00:00Z',
                    'likes_count': 0,
                    'comments_count': 0
                },
                response_only=True
            ),
        ]
    ),
    update=extend_schema(
        summary='Обновить пост',
        description='Полное обновление поста',
        request=BlogPostSerializer,
        tags=['Posts'],
        examples=[
            OpenApiExample(
                'Пример запроса',
                value={
                    'title': 'Новый заголовок',
                    'text': 'Новый текст'
                },
                request_only=True
            ),
            OpenApiExample(
                'Пример ответа',
                value={
                    'id': '550e8400-e29b-41d4-a716-446655440000',
                    'title': 'Новый заголовок',
                    'text': 'Новый текст',
                    'author': 'User',
                    'created_at': '2026-04-19T12:00:00Z',
                    'updated_at': '2026-04-19T12:05:00Z',
                    'likes_count': 0,
                    'comments_count': 0
                },
                response_only=True
            ),
        ]
    ),
    partial_update=extend_schema(
        summary='Частично обновить пост',
        description='Частичное обновление',
        request=BlogPostSerializer,
        tags=['Posts'],
        examples=[
            OpenApiExample(
                'Пример запроса',
                value={'title': 'Новый заголовок'},
                request_only=True
            ),
            OpenApiExample(
                'Частичное обновление',
                value={
                    'id': '550e8400-e29b-41d4-a716-446655440000',
                    'title': 'Новый заголовок',
                    'text': 'Новый текст',
                    'author': 'User',
                    'created_at': '2026-04-19T12:00:00Z',
                    'updated_at': '2026-04-19T12:05:00Z',
                    'likes_count': 0,
                    'comments_count': 0
                },
                request_only=True
            )
        ]
    ),
    destroy=extend_schema(
        summary='Удалить пост',
        description='Удалить пост.',
        tags=['Posts'],
        examples=[
            OpenApiExample(
                'Успешное удаление',
                description='',
                response_only=True,
                status_codes=['204']
            )
        ]
    ),
)

like_docs = dict(
    summary='Лайк',
    description='Лайки пользователей',
    methods=['POST', 'DELETE'],
    request=None,
    tags=['Likes'],
    examples=[
        OpenApiExample(
            'Поставить лайк',
            value={
                'status': 'liked',
                'likes_count': 1
            },
            response_only=True,
            status_codes=['201']
        ),
        OpenApiExample(
            'Убрать лайк',
            value={
                'status': 'unliked',
                'likes_count': 0
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)

comment_docs = dict(
    list=extend_schema(
        summary='Список комментариев',
        description='Получить список всех комментариев с возможностью фильтрации и сортировки',
        parameters=[
            OpenApiParameter(name='author__username', description='Фильтр по автору', type=str, required=False),
            OpenApiParameter(name='created_at', description='Фильтр по (YYYY-MM-DD)', type=str, required=False),
            OpenApiParameter(name='created_at_gte', description='Фильтр по дате "от" (YYYY-MM-DD)', type=str, required=False),
            OpenApiParameter(name='created_at_lte', description='Фильтр по дате "до" (YYYY-MM-DD)', type=str, required=False),
            OpenApiParameter(
                name='ordering',
                description='Сортировка: created_at, -created_at, author__username, -author__username',
                type=str,
                required=False
            ),
        ],
        tags=['Comments'],
        examples=[
            OpenApiExample(
                'Список комментариев',
                value=[
                    {
                        'id': '2c02edb7-7244-4fcf-9ec0-9d57f691e124',
                        'author': 'User',
                        'post': 'b86a48e5-8f77-467f-a24c-f3ccbddb095c',
                        'text': 'Текст',
                        'created_at': '2026-04-19T01:01:21.748544Z',
                        'updated_at': '2026-04-19T01:01:21.748553Z'
                    }
                ],
                response_only=True
            ),
        ]
    ),
    create=extend_schema(
        summary='Создать комментарий',
        description='Создать новый комментарий к посту',
        request=CommentSerializer,
        tags=['Comments'],
        examples=[
            OpenApiExample(
                'Пример запроса',
                value={
                    'text': 'Новый коммент',
                    'post': '550e8400-e29b-41d4-a716-446655440000'
                },
                request_only=True
            ),
            OpenApiExample(
                'Пример ответа',
                value={
                    'id': '2c02edb7-7244-4fcf-9ec0-9d57f691e124',
                    'author': 'User',
                    'post': 'b86a48e5-8f77-467f-a24c-f3ccbddb095c',
                    'text': 'Текст',
                    'created_at': '2026-04-19T01:01:21.748544Z',
                    'updated_at': '2026-04-19T01:01:21.748553Z'
                },
                response_only=True,
                status_codes=['201']
            )
        ]
    ),
    retrieve=extend_schema(
        summary='Получить комментарий',
        description='Получить детальную информацию о комментарии по ID',
        tags=['Comments'],
        examples=[
            OpenApiExample(
                'Детали комментария',
                value={
                    'id': '2c02edb7-7244-4fcf-9ec0-9d57f691e124',
                    'author': 'User',
                    'post': 'b86a48e5-8f77-467f-a24c-f3ccbddb095c',
                    'text': 'Текст',
                    'created_at': '2026-04-19T01:01:21.748544Z',
                    'updated_at': '2026-04-19T01:01:21.748553Z'
                },
                response_only=True
            )
        ]
    ),
    update=extend_schema(
        summary='Обновить комментарий',
        description='Полное обновление комментария',
        request=CommentSerializer,
        tags=['Comments'],
        examples=[
            OpenApiExample(
                'Обновление комментария',
                value={'text': 'Обновленный текст комментария'},
                request_only=True
            ),
            OpenApiExample(
                'Пример ответа',
                value={
                    'id': '2c02edb7-7244-4fcf-9ec0-9d57f691e124',
                    'author': 'User',
                    'post': 'b86a48e5-8f77-467f-a24c-f3ccbddb095c',
                    'text': 'Обновленный текст комментария',
                    'created_at': '2026-04-19T01:01:21.748544Z',
                    'updated_at': '2026-04-19T01:01:21.748553Z'
                },
                response_only=True
            )
        ]
    ),
    partial_update=extend_schema(
        summary='Частично обновить комментарий',
        description='Частичное обновление комментария',
        request=CommentSerializer,
        tags=['Comments'],
        examples=[
            OpenApiExample(
                'Частичное обновление',
                value={
                    'id': '79d2369a-779f-46d6-8b8b-20653b32e3e4',
                    'author': 'User',
                    'post': '74dab514-0574-4cb6-a880-b0606a0a371b',
                    'text': 'Новый текст',
                    'created_at': '2026-04-19T02:13:12.157374Z',
                    'updated_at': '2026-04-19T02:16:31.131244Z'
                },
                request_only=True
            )
        ]
    ),
    destroy=extend_schema(
        summary='Удалить комментарий',
        description='Удалить комментарий',
        tags=['Comments'],
        examples=[
            OpenApiExample(
                'Успешное удаление',
                description='Возвращает статус 204',
                response_only=True,
                status_codes=['204']
            )
        ]
    ),
)