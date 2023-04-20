from django.test import TestCase

from ..models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_post_correct_object_names(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        self.assertEqual(self.post.__str__(), 'Тестовый пост'[:15])

    def test_group_correct_object_names(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        self.assertEqual(self.group.__str__(), 'Тестовая группа')

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        field_verboses = {
            'pub_date': 'Дата создания',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, expected in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).verbose_name, expected)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        self.assertEqual(
            self.post._meta.get_field('group').help_text, 'Группа поста')
