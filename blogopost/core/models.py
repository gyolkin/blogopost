from django.db import models


class PostCommentModel(models.Model):
    """Базовая модель для записей и комментариев."""
    text = models.TextField(
        verbose_name='Текст публикации'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)
        indexes = [
            models.Index(fields=['-pub_date']),
        ]

    def __str__(self):
        return self.text[:15]
