from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, CommentViewSet


router = DefaultRouter()
router.register('posts', BlogPostViewSet, basename="posts")
router.register('comments', CommentViewSet, basename='comments')
