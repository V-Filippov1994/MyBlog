import uuid

from ckeditor.fields import RichTextField

from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = RichTextField(verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="likes", verbose_name='Пост')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('author', 'post')

    def __str__(self):
        return f'{self.author.username} - {self.post.title}'


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments", verbose_name='Пост')
    text = RichTextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        unique_together = ('author', 'post')

    def __str__(self):
        return f'{self.author.username} - {self.post.title}'