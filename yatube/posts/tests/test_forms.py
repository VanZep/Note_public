import shutil
import tempfile

from django.urls import reverse
from django.conf import settings
from django.test import TestCase, Client, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Post, Group, User, Comment


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class FormsTests(TestCase):
    """Тестирует формы."""

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
            text='Тестовый текст поста',
            author=cls.user,
            group=cls.group,
        )
        cls.comment = Comment.objects.create(
            text='Тестовый комментарий',
            post=cls.post,
            author=cls.user
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(FormsTests.user)

    def test_create_post_with_picture(self):
        """Валидная форма создает запись с картинкой в Post."""
        gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='gif.gif',
            content=gif,
            content_type='image/gif'
        )
        form_data = {
            'text': FormsTests.post.text,
            'group': FormsTests.group.pk,
            'image': uploaded
        }
        all_posts_before_create = set(Post.objects.all())
        response = self.auth_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        set_posts = set(Post.objects.all()).difference(
            all_posts_before_create
        )
        self.assertRedirects(
            response, reverse(
                'posts:profile', kwargs={
                    'username': FormsTests.post.author
                }
            )
        )
        self.assertEqual(len(set_posts), 1)
        self.assertTrue(
            Post.objects.filter(
                pk=next(iter(set_posts)).pk,
                text=next(iter(set_posts)).text,
                group=next(iter(set_posts)).group,
                author=next(iter(set_posts)).author,
                image=next(iter(set_posts)).image
            ).exists()
        )

    def test_post_edit(self):
        """Валидная форма изменяет запись в Post."""
        posts_count = Post.objects.count()
        new_group = Group.objects.create(slug='new-group-slug')
        form_data = {
            'text': 'Новый текст поста',
            'group': new_group.pk,
        }
        response = self.auth_client.post(
            reverse(
                'posts:post_edit', kwargs={
                    'post_id': FormsTests.post.pk
                }
            ),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse(
                'posts:post_detail', kwargs={
                    'post_id': FormsTests.post.pk
                }
            )
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                group=form_data['group'],
                author=FormsTests.post.author,
                pk=FormsTests.post.pk,
            ).exists()
        )

    def test_add_comment(self):
        """Валидная форма создает запись в Comment."""
        form_data = {
            'text': 'Новый комментарий',
            'author': FormsTests.comment.author
        }
        all_comments_before_create = set(Comment.objects.all())
        response = self.auth_client.post(
            reverse(
                'posts:add_comment', kwargs={
                    'post_id': FormsTests.post.pk
                }
            ),
            data=form_data
        )
        set_comments = set(Comment.objects.all()).difference(
            all_comments_before_create
        )
        self.assertRedirects(
            response, reverse(
                'posts:post_detail', kwargs={
                    'post_id': FormsTests.post.pk
                }
            )
        )
        self.assertEqual(len(set_comments), 1)
        self.assertTrue(
            Comment.objects.filter(pk=set_comments.pop().pk).exists()
        )
