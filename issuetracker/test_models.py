from django.contrib.auth.models import User
from django.test import TestCase
from .models import Ticket, Contribution, Vote

class TestModels(TestCase):
    """
    Runs tests against the 'Ticket', 'Contribution' and 'Vote' models
    """
    def setUp(self):
        self.user = User.objects.create(username = "user", email = "user@example.com", password = "password")
        self.user.save()
        self.bug = Ticket.objects.create(created_by = self.user, title = 'bug', description = 'bug description', ticket_type = 'Bug')
        self.feature = Ticket.objects.create(created_by = self.user, title = 'feature', description = 'feature description', ticket_type = 'Feature')
        self.bug.save()
        self.feature.save()

    def test_bug_and_feature_are_both_instances_of_a_Ticket(self):
        self.assertIsInstance(self.bug, Ticket)
        self.assertIsInstance(self.feature, Ticket)
    
    def test_title_and_description_are_both_strings(self):
        self.assertIsInstance(self.bug.title, str)
        self.assertIsInstance(self.bug.description, str)
    
    def test_Ticket_defaults(self):
        self.assertEqual(self.bug.url, '')
        self.assertEqual(self.bug.price, 20)
        self.assertEqual(self.bug.status, 'To do')
        self.assertEqual(self.bug.status_colour, 'dark')
        self.assertEqual(self.bug.completion, 0)
    
    def test_voting_on_a_Ticket_correctly_adds_Vote(self):
        self.assertEqual(Vote.objects.all().filter(ticket=self.bug).count(), 0)
        Vote.objects.create(user = self.user, ticket = self.bug)
        self.assertEqual(Vote.objects.all().filter(ticket=self.bug).count(), 1)
    
    def test_contributing_to_feature_correctly_adds_Contribution(self):
        self.assertEqual(Contribution.objects.all().filter(ticket=self.feature).count(), 0)
        Contribution.objects.create(user = self.user, ticket = self.feature, amount = 2)
        self.assertEqual(Contribution.objects.all().filter(ticket=self.feature).count(), 1)
        self.assertEqual(Contribution.objects.all().filter(ticket=self.feature)[0].amount, 2)