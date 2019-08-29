from django.test import TestCase
from .views import login, logout, register


class TestAddPostForm(TestCase):
    """
    Runs tests against the 'login', 'logout' and 'register' views
    """
    def test_user_logout_redirects_to_login(self):
        page = self.client.get("/accounts/logout/")
        self.assertEqual(page.status_code, 302)
        self.assertRedirects(page, "/accounts/login/?next=/accounts/logout/")

    def test_get_login_page_loads_correct_template(self):
        page = self.client.get("/accounts/login/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "login.html")

    def test_get_register_page_loads_correct_template(self):
        page = self.client.get("/accounts/register/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "register.html")
