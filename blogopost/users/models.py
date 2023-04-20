from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    avatar = models.ImageField(
        default='default.jpg',
        upload_to='profile_images',
        verbose_name='Аватар'
    )
    bio = models.TextField(
        max_length=500,
        verbose_name='Описание профиля',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse(
            'posts:profile',
            kwargs={'username': self.user.username}
        )
