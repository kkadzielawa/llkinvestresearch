from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Post


@override_settings(SECURE_SSL_REDIRECT=False)
class PostVisibilityTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="konrad",
            email="konrad@example.com",
            password="password123",
        )
        self.published_post = Post.objects.create(
            title="Published Research",
            slug="published-research",
            author=self.user,
            content="<p>Published body</p>",
            status=Post.PostStatus.PUBLISHED,
        )
        self.draft_post = Post.objects.create(
            title="Draft Research",
            slug="draft-research",
            author=self.user,
            content="<p>Draft body</p>",
            status=Post.PostStatus.DRAFT,
        )

    def test_published_post_appears_in_blog_list(self):
        response = self.client.get(reverse("blog"))
        self.assertContains(response, self.published_post.title)

    def test_draft_post_does_not_appear_in_blog_list(self):
        response = self.client.get(reverse("blog"))
        self.assertNotContains(response, self.draft_post.title)

    def test_published_post_detail_returns_200(self):
        response = self.client.get(self.published_post.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_draft_post_detail_returns_404(self):
        response = self.client.get(reverse("post_detail", args=[self.draft_post.slug]))
        self.assertEqual(response.status_code, 404)

    def test_posts_are_ordered_newest_first(self):
        newer_post = Post.objects.create(
            title="Newest Note",
            slug="newest-note",
            author=self.user,
            content="<p>Newest body</p>",
            status=Post.PostStatus.PUBLISHED,
        )
        response = self.client.get(reverse("blog"))
        posts = list(response.context["posts"])
        self.assertEqual(posts[0], newer_post)
