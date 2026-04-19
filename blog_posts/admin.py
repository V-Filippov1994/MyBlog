from django.contrib import admin

from .models import BlogPost, Comment, Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at',)
    list_filter = ('author', 'post',)
    readonly_fields = ('id', 'created_at', 'author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'updated_at',)
    autocomplete_fields = ('author',)
    search_fields = ('text',)
    list_filter = ('author', 'created_at')
    readonly_fields = ('id', 'updated_at', 'created_at', 'author',)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'updated_at',)
    autocomplete_fields = ('author',)
    search_fields = ('title', 'text',)
    list_filter = ('author', 'created_at')
    readonly_fields = ('id', 'updated_at', 'created_at', 'author',)
    inlines = (CommentInline, )
