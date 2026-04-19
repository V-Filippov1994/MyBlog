from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse


github_auth_docs = dict(
    github_login=extend_schema(
        summary='GitHub авторизация',
        description='Авторизация пользователей через GitHub',
        tags=['Authentication'],
        responses={
            200: OpenApiResponse(
                description='URL для авторизации',
                response={
                    'type': 'object',
                    'properties': {
                        'authorization_url': {'type': 'string',
                                              'example': 'https://github.com/login/oauth/authorize?client_id='}
                    }
                }
            )
        },
        examples=[
            OpenApiExample(
                'Успешный ответ',
                value={
                    'authorization_url': 'https://github.com/login/oauth/authorize?client_id=xxx&redirect_uri=http://localhost:8000/api/auth/github/callback/&scope=read:user user:email&state=abc123'
                },
                response_only=True
            ),
            OpenApiExample(
                'Ошибка конфигурации',
                value={'error': 'Not configured'},
                response_only=True,
                status_codes=['409']
            )
        ]
    ),
    github_callback=extend_schema(
        summary='GitHub Callback',
        description='Callback от GitHub после авторизации',
        tags=['Authentication'],
        parameters=[
            OpenApiParameter(name='code', description='Код авторизации от GitHub', type=str, required=True,
                             location=OpenApiParameter.QUERY),
            OpenApiParameter(name='state', description='State параметр для защиты от CSRF', type=str, required=True,
                             location=OpenApiParameter.QUERY),
        ],
        examples=[
            OpenApiExample(
                'Успешная авторизация',
                description='Перенаправляет на LOGIN_REDIRECT_URL',
                response_only=True,
                status_codes=['302']
            )
        ]
    ),
    status=extend_schema(
        summary='Статус авторизации',
        description='Проверяет авторизован ли текущий пользователь',
        tags=['Authentication'],
        responses={
            200: OpenApiResponse(
                description='Пользователь авторизован',
                response={
                    'type': 'object',
                    'properties': {
                        'authenticated': {'type': 'boolean', 'example': True},
                        'user_id': {'type': 'integer', 'example': 1},
                        'username': {'type': 'string', 'example': 'john_doe'},
                        'email': {'type': 'string', 'example': 'vasya@mail.ru'},
                    }
                }
            ),
            401: OpenApiResponse(
                description='Пользователь не авторизован',
                response={'authenticated': False}
            ),
        },
        examples=[
            OpenApiExample(
                'Авторизован',
                value={
                    'authenticated': True,
                    'user_id': 1,
                    'username': 'vasya',
                    'email': 'vasya@mail.ru'
                },
                response_only=True,
                status_codes=['200']
            ),
            OpenApiExample(
                'Не авторизован',
                value={'authenticated': False},
                response_only=True,
                status_codes=['401']
            )
        ]
    ),
    logout=extend_schema(
        summary="Выход",
        description="Завершает сессию пользователя",
        tags=['Authentication'],
        responses={
            302: OpenApiResponse(description='Успешный выход, перенаправление на LOGIN_REDIRECT_URL'),
        },
        examples=[
            OpenApiExample(
                'GET запрос (редирект)',
                description='Перенаправляет на LOGIN_REDIRECT_URL',
                response_only=True,
                status_codes=['302']
            ),
        ]
    )
)