from django.contrib.auth.models import User
from django.test import TestCase
from .models import Post


class TestPost(TestCase):
    """
    Runs tests against the 'Post' model
    """
    def setUp(self):
        self.author = User.objects.create(
            username="user",
            email="user@example.com",
            password="password")
        self.author.save()
        self.post = Post.objects.create(
            title="Post",
            author=self.author,
        )
        self.post.save()

    def test_post_is_a_Post_with_an_author_that_is_a_User(self):
        test_post = self.post
        self.assertIsInstance(test_post, Post)
        self.assertIsInstance(test_post.author, User)

    def test_post_title_is_a_string_called_Post(self):
        test_post = self.post
        self.assertEqual(test_post.title, "Post")
        self.assertIsInstance(test_post.title, str)

    def test_post_default_views_is_zero(self):
        test_post = self.post
        self.assertEqual(test_post.views, 0)
