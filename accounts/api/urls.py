from rest_framework.routers import DefaultRouter
from accounts.api.views import GitHubAuthViewSet


router = DefaultRouter()
router.register('auth', GitHubAuthViewSet, basename='auth')