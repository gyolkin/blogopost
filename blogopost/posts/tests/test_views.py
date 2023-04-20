import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageFieldFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Follow, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
small_gif = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B')


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.suser = User.objects.create_user(username='suser')
        uploaded_gif = SimpleUploadedFile(name='small.gif',
                                          content=small_gif,
                                          content_type='image/gif')
        group_objs = [
            Group(
                title=f"Тестовая группа {i}",
                slug=f"slug{i}"
            )
            for i in range(1, 3)
        ]
        cls.groups = Group.objects.bulk_create(group_objs)
        post_objs = [
            Post(
                text='Тестовый текст',
                author=cls.user,
                image=uploaded_gif,
                group=Group.objects.get(title='Тестовая группа 1')
            )
            for i in range(1, 12)
        ]
        cls.posts = Post.objects.bulk_create(post_objs)
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.suser,
            image=uploaded_gif,
            group=Group.objects.get(title='Тестовая группа 2'))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.auth = Client()
        self.auth.force_login(self.user)

    def test_namespace(self):
        """Проверка namespace."""
        namespace = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    args=(self.groups[0].slug,)): 'posts/group_list.html',
            reverse('posts:profile',
                    args=(self.user.username,)): 'posts/profile.html',
            reverse('posts:post_detail',
                    args=(self.post.id,)): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit',
                    args=(1,)): 'posts/create_post.html',
        }
        for url, template in namespace.items():
            with self.subTest(address=url):
                response = self.auth.get(url)
                self.assertTemplateUsed(response, template)

    def test_context_index(self):
        """Проверка контекста index."""
        response = self.auth.get(reverse('posts:index'))
        obj = response.context['page_obj'][0]
        self.assertEqual(obj.text, 'Тестовый текст')
        self.assertIsInstance(obj.image, ImageFieldFile)

    def test_paginator_index_first_page(self):
        """Проверка пагинатора index. Первая страница."""
        response = self.auth.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_paginator_index_second_page(self):
        """Проверка пагинатора index. Вторая страница"""
        response = self.auth.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 2)

    def test_context_group_list(self):
        """Проверка контекста group_list. Проверка, что посты, предназначенные
        для другой группы не попадают в список постов данной группы."""
        response = self.auth.get(reverse(
            'posts:group_list',
            args=(self.groups[1].slug,)))
        for i in response.context['page_obj']:
            self.assertEqual(i.group.title, 'Тестовая группа 2')
        self.assertIsInstance(response.context['page_obj'][0].image,
                              ImageFieldFile)

    def test_paginator_group_list_first_page(self):
        """Проверка пагинатора group_list. Первая страница."""
        response = self.auth.get(reverse(
            'posts:group_list',
            args=(self.groups[0].slug,)))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_paginator_group_list_second_page(self):
        """Проверка пагинатора index. Вторая страница"""
        response = self.auth.get(reverse(
            'posts:group_list', args=(self.groups[0].slug,)) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_context_profile(self):
        """Проверка контекста profile."""
        response = self.auth.get(reverse(
            'posts:profile', args=(self.user.username,)))
        for i in response.context['page_obj']:
            self.assertEqual(i.author.username, 'auth')
        self.assertIsInstance(response.context['page_obj'][0].image,
                              ImageFieldFile)

    def test_paginator_profile_first_page(self):
        """Проверка пагинатора profile. Первая страница."""
        response = self.auth.get(reverse(
            'posts:profile', args=(self.user.username,)))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_paginator_profile_second_page(self):
        """Проверка пагинатора profile. Вторая страница."""
        response = self.auth.get(reverse(
            'posts:profile', args=(self.user.username,)) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_post_detail(self):
        """Проверка контекста post_detail. Один пост, выбранный по id."""
        response = self.auth.get(reverse(
            'posts:post_detail', args=(1,)))
        self.assertEqual(response.context['post'].text, 'Тестовый текст')
        self.assertIsInstance(response.context['post'].image, ImageFieldFile)

    def test_create_post(self):
        """Проверка соответствия полей при создании поста."""
        response = self.auth.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for val, exp in form_fields.items():
            with self.subTest(value=val):
                form_field = response.context.get('form').fields.get(val)
                self.assertIsInstance(form_field, exp)

    def test_edit_post(self):
        """Проверка соответствия полей при редактировании поста."""
        response = self.auth.get(reverse(
            'posts:post_edit', args=(1,)))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for val, exp in form_fields.items():
            with self.subTest(value=val):
                form_field = response.context.get('form').fields.get(val)
                self.assertIsInstance(form_field, exp)

    def test_subscription_follow(self):
        """Проверка работоспособности возможности подписки в модели Follow."""
        sub0 = Follow.objects.filter(author=self.suser).count()
        self.auth.get(reverse(
            'posts:profile_follow', args=(self.suser.username,)))
        sub1 = Follow.objects.filter(author=self.suser).count()
        self.auth.get(reverse(
            'posts:profile_follow', args=(self.suser.username,)))
        sub2 = Follow.objects.filter(author=self.suser).count()
        self.assertEqual(sub2, sub1, sub0 + 1)

    def test_subscription_unfollow(self):
        """Проверка работоспособности возможности отписки в модели Follow."""
        self.auth.get(reverse(
            'posts:profile_follow', args=(self.suser.username,)))
        sub0 = Follow.objects.filter(author=self.suser).count()
        self.auth.get(reverse(
            'posts:profile_unfollow', args=(self.suser.username,)))
        sub1 = Follow.objects.filter(author=self.suser).count()
        self.assertEqual(sub1, sub0 - 1)

    def test_subscription_feed(self):
        """Проверка корректности отображения ленты пользователей (запись
        появляется в ленте тех, кто подписан, и не появляется у тех, кто
        не подписан)."""
        self.authorized_suser = Client()
        self.authorized_suser.force_login(self.suser)
        self.auth.get(reverse(
            'posts:profile_follow', args=(self.suser.username,)))
        response_nofollow = self.authorized_suser.get(reverse(
            'posts:follow_index'))
        response_follow = self.auth.get(reverse(
            'posts:follow_index'))
        self.assertNotEqual(len(response_nofollow.context['page_obj']),
                            len(response_follow.context['page_obj']))

    def test_index_cache(self):
        """Проверка работы кеширования контента главной страницы."""
        response = self.auth.get(reverse('posts:index'))
        obj = response.content
        Post.objects.create(
            text='Кеширование',
            author=self.user
        )
        new_response = self.auth.get(reverse('posts:index'))
        new_obj = new_response.content
        cache.clear()
        no_response = self.auth.get(reverse('posts:index'))
        no_obj = no_response.content
        self.assertEqual(obj, new_obj)
        self.assertNotEqual(obj, no_obj)
