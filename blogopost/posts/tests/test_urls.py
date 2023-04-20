from http import HTTPStatus

from django.test import Client, TestCase

from ..models import Group, Post, User


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug'
        )

    def setUp(self):
        self.auth = Client()
        self.auth.force_login(self.user)

    def test_home_url(self):
        """Страница / доступна любому пользователю."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_slug(self):
        """Страница /group/<slug>/ доступна любому пользователю."""
        response = self.client.get('/group/slug/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_id(self):
        """Страница /profile/<user>/ доступна любому пользователю."""
        response = self.client.get('/profile/auth/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_id(self):
        """Страница /posts/<id>/ доступна любому пользователю."""
        response = self.client.get('/posts/1/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_edit_authorized(self):
        """Страница /posts/<id>/edit/ доступна автору."""
        response = self.auth.get('/posts/1/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_create_authorized(self):
        """Страница /create/ доступна авторизованному пользователю."""
        response = self.auth.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_not_found(self):
        """Страница 404 NOT FOUND доступна любому пользователю."""
        response = self.client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_not_found_template(self):
        """Страница 404 NOT FOUND отдает кастомный шаблон."""
        response = self.client.get('/unexisting_page/')
        self.assertTemplateUsed(response, 'core/404.html')

    def test_posts_templates(self):
        """Шаблоны для приложения posts отображаются правильно."""
        template_urls = {
            '/': 'posts/index.html',
            '/group/slug/': 'posts/group_list.html',
            '/profile/auth/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/posts/1/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for address, template in template_urls.items():
            with self.subTest(address=address):
                response = self.auth.get(address)
                self.assertTemplateUsed(response, template)
