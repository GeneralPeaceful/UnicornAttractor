from django.contrib.auth.models import User
from django.test import TestCase
from .views import (
    view_cart, add_to_cart, remove_from_cart, charge, update_cart)
from issuetracker.models import Ticket


class TestViews(TestCase):
    """
    Runs tests against views
    """
    def test_all_pages_require_login(self):
        page1 = self.client.get("/cart/")
        page2 = self.client.get("/cart/add/1/")
        page3 = self.client.get("/cart/remove/1/")
        page4 = self.client.get("/cart/update_cart/1/")
        page5 = self.client.get("/cart/charge/")
        self.assertEqual(page1.status_code, 302)
        self.assertEqual(page2.status_code, 302)
        self.assertEqual(page3.status_code, 302)
        self.assertEqual(page4.status_code, 302)
        self.assertEqual(page5.status_code, 302)
        self.assertRedirects(page1, "/accounts/login/?next=/cart/")
        self.assertRedirects(page2, "/accounts/login/?next=/cart/add/1/")
        self.assertRedirects(page3, "/accounts/login/?next=/cart/remove/1/")
        self.assertRedirects(
            page4, "/accounts/login/?next=/cart/update_cart/1/")
        self.assertRedirects(page5, "/accounts/login/?next=/cart/charge/")
