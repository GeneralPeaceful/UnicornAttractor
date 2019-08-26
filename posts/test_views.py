from django.contrib.auth.models import User
from django.test import TestCase
from .models import Post
from .views import get_posts, post_detail, create_post

class TestViews(TestCase):
    """
    Runs tests against views
    """
    def test_get_all_posts_home_page(self):
        page = self.client.get("/posts/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "posts.html")
    
    def test_get_post_detail_page(self):
        user = User.objects.create(username = "user", email = "user@example.com", password = "password")
        user.save()
        post = Post.objects.create(title = "title", author = user)
        post.save()
        page = self.client.get("/posts/{0}/".format(post.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "postdetail.html")
    
    def test_get_create_post_page_without_user_redirects_to_login(self):
        page = self.client.get("/posts/new/")
        self.assertEqual(page.status_code, 302)
        self.assertRedirects(page, "/accounts/login/?next=/posts/new/")