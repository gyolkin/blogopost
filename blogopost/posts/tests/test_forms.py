import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Comment, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.auth = Client()
        self.auth.force_login(self.user)

    def test_create_post_form(self):
        """Валидная форма создает запись в Post."""
        Post.objects.all().delete()
        tasks_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B')
        uploaded_gif = SimpleUploadedFile(name='small.gif',
                                          content=small_gif,
                                          content_type='image/gif')
        response = self.auth.post(
            reverse('posts:post_create'),
            data={'text': 'Тестовый текст', 'image': uploaded_gif},
            follow=True
        )
        self.assertRedirects(response, reverse('posts:profile',
                                               args=(self.user.username,)))
        self.assertEqual(Post.objects.count(), tasks_count + 1)

    def test_edit_post_form(self):
        """Проверка формы редактирования поста."""
        self.auth.post(
            reverse('posts:post_edit', args=(self.post.id,)),
            data={'text': 'Текст изменился'},
            follow=True
        )
        self.assertNotEqual(self.post.text,
                            Post.objects.get(pk=self.post.id).text)

    def test_create_comment(self):
        """Валидная форма Comment создает комментарий на странице поста."""
        comments_count = Comment.objects.filter(post=self.post.id).count()
        self.auth.post(
            reverse('posts:add_comment', args=(self.post.id,)),
            data={'text': 'Тестовый текст'},
            follow=True
        )
        self.assertEqual(Comment.objects.filter(post=self.post.id).count(),
                         comments_count + 1)

    def test_create_comment_unauthorized(self):
        """Комментарий может оставлять только авторизованный пользователь.
        Анонимный пользователь отправляется на страницу авторизации."""
        response = self.client.post(
            reverse('posts:add_comment', args=(self.post.id,)),
            data={'text': 'Тестовый текст'},
            follow=True
        )
        self.assertRedirects(response, '/auth/login/?next=/posts/1/comment/')
