from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse

from ..models import Post, Group, User


class URLTests(TestCase):
    """Тестирует URLs."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.user2 = User.objects.create_user(username='auth2')
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='test-slug',
            description='Тестовое описание группы'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст поста',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(URLTests.user)
        self.auth_client2 = Client()
        self.auth_client2.force_login(URLTests.user2)

    def test_anonymous_pages_urls(self):
        """Страницы index, group_list, profile, post_detail
        доступны любому пользователю.
        """
        urls = (
            '/',
            f'/group/{URLTests.group.slug}/',
            f'/profile/{URLTests.user.username}/',
            f'/posts/{URLTests.post.pk}/'
        )
        for url in urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexisting_page_url(self):
        """Несуществующая страница возвращает ошибку 404."""
        response = self.client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_post_create_url_authorized(self):
        """Страница post_create доступна авторизованному пользователю."""
        response = self.auth_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_url_authorized(self):
        """Страница post_edit доступна авторизованному пользователю."""
        if URLTests.post.author == URLTests.user:
            response = self.auth_client.get(f'/posts/{URLTests.post.pk}/edit/')
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_add_comment_url_authorized(self):
        """Страница add_comment доступна авторизованному пользователю."""
        response = self.auth_client.get(f'/posts/{URLTests.post.pk}/comment/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_post_create_url_redirect_anonymous_on_login(self):
        """Страница post_create перенаправит анонимного
        пользователя на страницу login.
        """
        response = self.client.get(reverse('posts:post_create'), follow=True)
        self.assertRedirects(
            response, reverse('users:login') + '?next='
            + reverse('posts:post_create')
        )

    def test_post_edit_url_redirect_anonymous_on_login(self):
        """Страница post_edit перенаправит анонимного
        пользователя на страницу login.
        """
        response = self.client.get(
            reverse('posts:post_edit', kwargs={'post_id': URLTests.post.pk}),
            follow=True
        )
        self.assertRedirects(
            response, reverse('users:login') + '?next='
            + reverse('posts:post_edit', kwargs={'post_id': URLTests.post.pk})
        )

    def test_post_edit_url_redirect_anonymous_on_login(self):
        """Страница post_edit перенаправит авторизованного пользователя
        на страницу post_detail, если он пытается редактировать чужой пост.
        """
        response = self.auth_client2.get(
            reverse('posts:post_edit', kwargs={'post_id': URLTests.post.pk}),
            follow=True
        )
        self.assertRedirects(
            response, (
                reverse(
                    'posts:post_detail', kwargs={'post_id': URLTests.post.pk}
                )
            )
        )

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{URLTests.group.slug}/': 'posts/group_list.html',
            f'/profile/{URLTests.user.username}/': 'posts/profile.html',
            f'/posts/{URLTests.post.pk}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{URLTests.post.pk}/edit/': 'posts/create_post.html'
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.auth_client.get(address)
                self.assertTemplateUsed(response, template)
