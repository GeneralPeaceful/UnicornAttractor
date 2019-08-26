from django.contrib.auth.models import User
from django.test import TestCase
from .forms import AddPostForm

class TestAddPostForm(TestCase):
    """
    Runs tests against the 'AddPostForm' form
    """
    def setUp(self):
        self.author = User.objects.create(username = "user", email = "user@example.com", password = "password")
        self.author.save()
    
    def test_creating_post_with_only_author_displays_correct_error_messages(self):
        form = AddPostForm({'title': '', 'author': self.author, 'content': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], [u'This field is required.'])
        self.assertEqual(form.errors['content'], [u'This field is required.'])
    
    def test_can_create_post_without_tags(self):
        form = AddPostForm({'title': 'title', 'author': self.author, 'content': 'content', 'tags': ''})
        self.assertTrue(form.is_valid())