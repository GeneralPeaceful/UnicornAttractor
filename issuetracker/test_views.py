from django.contrib.auth.models import User
from django.test import TestCase
from .models import Ticket, Vote, Contribution
from .views import bugs, features, bug, feature, add_bug, add_feature, add_vote, edit_bug, edit_feature

class TestViews(TestCase):
    """
    Runs tests against views
    """
    def test_login_not_required_views_get_correct_templates(self):
        user = User.objects.create(username = 'user1', email = 'user1@example.com', password = 'password1')
        bug = Ticket.objects.create(created_by = user, title = 'bug', description = 'bug description', ticket_type = 'bug', status = 'PENDING', status_colour = 'dark')
        feature = Ticket.objects.create(created_by = user, title = 'feature', description = 'feature description', ticket_type = 'feature', status = 'PENDING', status_colour = 'dark')
        page1 = self.client.get("/bugs_&_features/bugs")
        page2 = self.client.get("/bugs_&_features/features")
        page3 = self.client.get("/bugs_&_features/bug/1/")
        page4 = self.client.get("/bugs_&_features/feature/1/")
        self.assertEqual(page1.status_code, 200)
        self.assertEqual(page2.status_code, 200)
        self.assertEqual(page3.status_code, 200)
        self.assertEqual(page4.status_code, 200)
        self.assertTemplateUsed(page1, "bugs.html")
        self.assertTemplateUsed(page2, "features.html")
        self.assertTemplateUsed(page3, "bug.html")
        self.assertTemplateUsed(page4, "feature.html")
    
    def test_login_required_views_redirect_to_login(self):
        page1 = self.client.get("/bugs_&_features/addbug")
        page2 = self.client.get("/bugs_&_features/addfeature")
        page3 = self.client.get("/bugs_&_features/addvote/1/")
        page4 = self.client.get("/bugs_&_features/editbug/1/")
        page5 = self.client.get("/bugs_&_features/editfeature/2/")
        self.assertEqual(page1.status_code, 302)
        self.assertEqual(page2.status_code, 302)
        self.assertEqual(page3.status_code, 302)
        self.assertEqual(page4.status_code, 302)
        self.assertEqual(page5.status_code, 302)
        self.assertRedirects(page1, "/accounts/login/?next=/bugs_%26_features/addbug")
        self.assertRedirects(page2, "/accounts/login/?next=/bugs_%26_features/addfeature")
        self.assertRedirects(page3, "/accounts/login/?next=/bugs_%26_features/addvote/1/")
        self.assertRedirects(page4, "/accounts/login/?next=/bugs_%26_features/editbug/1/")
        self.assertRedirects(page5, "/accounts/login/?next=/bugs_%26_features/editfeature/2/")