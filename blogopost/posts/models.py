from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from core.models import PostCommentModel

User = get_user_model()


class Post(PostCommentModel):
    """Модель записи в блоге, наследуется от PostCommentModel."""
    title = models.CharField(
        max_length=60,
        verbose_name='Название публикации'
    )
    group = models.ForeignKey(
        'Group',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой подходит публикация'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    image = models.ImageField(
        verbose_name='Иллюстрация',
        upload_to='posts/',
        blank=True
    )

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'post_id': self.pk})


class Group(models.Model):
    """Модель для объединения записей в группы."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:group_list', kwargs={'slug': self.slug})


class Comment(PostCommentModel):
    """Модель комментирования, наследуется от PostCommentModel."""
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарии'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )


class Follow(models.Model):
    """Модель для подписки пользователей друг на друга."""
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )
