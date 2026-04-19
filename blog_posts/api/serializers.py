from rest_framework import serializers

from ..models import BlogPost, Comment, Like


class BlogPostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'text', 'author', 'created_at', 'updated_at', 'likes_count', 'comments_count')
        read_only_fields = ('created_at', 'updated_at')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_author(self, obj):
        return getattr(obj.author, "username", None)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'created_at',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created_at', 'updated_at')

    def get_author(self, obj):
        return obj.author.username

