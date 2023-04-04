from django.test import TestCase

from ..models import Post, Group, User, Comment
from ..constants import NUMBER_OF_CHAR


class ModelsTests(TestCase):
    """Тестирует модели."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='test-slug',
            description='Тестовое описание группы',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст поста',
        )
        cls.comment = Comment.objects.create(
            text='Тестовый комментарий',
            post=cls.post,
            author=cls.user
        )

    def test_post_model_have_correct_object_text(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        self.assertEqual(
            ModelsTests.post.text[:NUMBER_OF_CHAR], str(ModelsTests.post)
        )

    def test_group_model_have_correct_object_title(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        self.assertEqual(
            ModelsTests.group.title, str(ModelsTests.group)
        )

    def test_comment_model_have_correct_object_title(self):
        """Проверяем, что у модели Comment корректно работает __str__."""
        self.assertEqual(
            ModelsTests.comment.text[:NUMBER_OF_CHAR], str(ModelsTests.comment)
        )

    def test_post_model_verbose_name(self):
        """verbose_name в полях модели Post совпадает с ожидаемым."""
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации поста',
            'author': 'Автор поста',
            'group': 'Группa',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    ModelsTests.post._meta.get_field(value).verbose_name, (
                        expected
                    )
                )

    def test_group_model_verbose_name(self):
        """verbose_name в полях модели Group совпадает с ожидаемым."""
        field_verboses = {
            'title': 'Название группы',
            'slug': 'Уникальная часть адреса группы',
            'description': 'Описание группы',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    ModelsTests.group._meta.get_field(value).verbose_name, (
                        expected
                    )
                )

    def test_comment_model_verbose_name(self):
        """verbose_name в полях модели Comment совпадает с ожидаемым."""
        field_verboses = {
            'text': 'Текст комментария',
            'created': 'Дата публикации комментария',
            'post': 'Пост, к которому относится комментарий',
            'author': 'Автор комментария'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    ModelsTests.comment._meta.get_field(value).verbose_name, (
                        expected
                    )
                )

    def test_post_model_help_text(self):
        """help_text в полях модели Post совпадает с ожидаемым."""
        field_help_texts = {
            'text': 'Введите текст поста',
            'author': 'Автор, опубликовавший пост',
            'group': 'Группа, к которой будет относиться пост',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    ModelsTests.post._meta.get_field(value).help_text, (
                        expected
                    )
                )
