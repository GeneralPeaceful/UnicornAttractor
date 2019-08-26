from django.contrib.auth.models import User
from django.test import TestCase
from .models import Comment
from posts.models import Post

class TestComment(TestCase):
    """
    Runs tests against the 'Comment' model
    """
    def setUp(self):
        self.user = User.objects.create(username = "user", email = "user@example.com", password = "password")
        self.user.save()
        self.post = Post.objects.create(
            title = "Post",
            author = self.user,
        )
        self.post.save()
        self.comment = Comment.objects.create(user = self.user, comment = "A comment")
        self.comment.save()
    
    def test_comment_is_a_Comment_with_a_user_that_is_a_User(self):
        self.assertIsInstance(self.comment, Comment)
        self.assertIsInstance(self.comment.user, User)
    
    def test_comment_is_a_string_saying_A_comment(self):
        self.assertEqual(self.comment.comment, "A comment")
        self.assertIsInstance(self.comment.comment, str)