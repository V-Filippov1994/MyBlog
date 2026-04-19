from drf_spectacular.utils import extend_schema_view
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import login, logout, get_user_model
from urllib.parse import urlencode
import requests
import secrets

from accounts.swagger_docs import github_auth_docs

User = get_user_model()


@extend_schema_view(**github_auth_docs)
class GitHubAuthViewSet(ViewSet):
    @action(detail=False, methods=['get'], url_path='github/login')
    def github_login(self, request):
        if not settings.GITHUB_CLIENT_ID or not settings.GITHUB_CALLBACK_URL:
            return Response(data={'error': 'Not configured'}, status=status.HTTP_409_CONFLICT)

        state = secrets.token_urlsafe(32)
        request.session['github_oauth_state'] = state
        config = {
            'client_id': settings.GITHUB_CLIENT_ID,
            'redirect_uri': request.build_absolute_uri(settings.GITHUB_CALLBACK_URL),
            'scope': 'read:user user:email',
            'state': state,
        }
        auth_url = 'https://github.com/login/oauth/authorize?' + urlencode(config)
        return Response({'authorization_url': auth_url})

    @action(detail=False, methods=['get'], url_path='github/callback')
    def github_callback(self, request):
        code = request.GET.get('code')
        state = request.GET.get('state')
        stored_state = request.session.get('github_oauth_state')
        if not state or state != stored_state:
            return Response(data={'error': 'Invalid state parameter'}, status=status.HTTP_400_BAD_REQUEST)

        token_url = 'https://github.com/login/oauth/access_token'
        headers = {'Accept': 'application/json'}
        data = {
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
            'code': code,
            'redirect_uri': request.build_absolute_uri(settings.GITHUB_CALLBACK_URL),
        }

        response = requests.post(token_url, data=data, headers=headers)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get('access_token')
        if not access_token:
            return Response(
                {'error': 'No access token received'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_url = 'https://api.github.com/user'
        user_headers = {'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
        user_response = requests.get(user_url, headers=user_headers)
        user_response.raise_for_status()
        github_user = user_response.json()
        email_url = 'https://api.github.com/user/emails'
        email_response = requests.get(email_url, headers=user_headers)
        email_response.raise_for_status()
        emails = email_response.json()
        primary_email = None
        for email in emails:
            if email.get('primary'):
                primary_email = email.get('email')
                break

        if not primary_email:
            primary_email = github_user.get('email', '')
        username = github_user.get('login')
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': primary_email or '',
                'first_name': github_user.get('name', '').split()[0] if github_user.get('name') else '',
                'last_name': ' '.join(github_user.get('name', '').split()[1:]) if github_user.get('name') else '',
            }
        )
        login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)

    @action(detail=False, methods=['get'], url_path='status')
    def status(self, request):
        if request.user.is_authenticated:
            return Response({
                'authenticated': True,
                'user_id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
            })
        return Response(data={'authenticated': False}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'], url_path='logout')
    def logout(self, request):
        logout(request)
        if request.method == 'POST':
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        return redirect(settings.LOGIN_REDIRECT_URL)
