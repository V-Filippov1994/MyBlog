from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.db.models import Count

from .filters import BlogPostFilterSet, CommentFilter
from .permissions import CustomAuthorPermission
from .serializers import BlogPostSerializer, CommentSerializer, LikeSerializer

from ..models import BlogPost, Comment, Like
from ..swagger_docs import blog_post_docs, like_docs, comment_docs


@extend_schema_view(**blog_post_docs)
class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.select_related('author').all().order_by("-created_at")
    serializer_class = BlogPostSerializer
    permission_classes = [CustomAuthorPermission]
    filterset_class = BlogPostFilterSet
    ordering_fields = ['created_at', 'likes_count', 'comments_count', 'title']

    def get_queryset(self):
        return self.queryset.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(**like_docs)
    @action(detail=True,
            methods=['post', 'delete'],
            url_path='like',
            serializer_class=LikeSerializer,
            permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like = Like.objects.filter(author=request.user, post=post)
        if request.method == 'POST':
            if like.exists():
                return Response(data={'error': 'Like exists'}, status=status.HTTP_400_BAD_REQUEST)

            Like.objects.create(author=request.user, post=post)
            return Response(
                data={'status': 'liked', 'likes_count': post.likes.count()},
                status=status.HTTP_201_CREATED
            )
        else:
            if not like.exists():
                return Response(data={'error': 'Like does not exists'}, status=status.HTTP_400_BAD_REQUEST)

            like.delete()
            return Response(
                data={'status': 'unliked', 'likes_count': post.likes.count()},
                status=status.HTTP_200_OK
            )


@extend_schema_view(**comment_docs)
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related('author', 'post').all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [CustomAuthorPermission]
    ordering_fields = ['created_at', 'author__username', 'post__title']
    filterset_class = CommentFilter

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = get_object_or_404(BlogPost, id=post_id)
        if Comment.objects.filter(author=self.request.user, post=post).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'error': 'You have already commented on this post'})
        serializer.save(author=self.request.user, post=post)