from django.contrib.auth.models import User
from django.test import TestCase
from .forms import (
    ReportBugForm, StaffReportBugForm,
    RequestFeatureForm, StaffRequestFeatureForm)


class TestForms(TestCase):
    """
    Runs tests against the 'ReportBugForm', 'RequestFeatureForm',
    'StaffReportBugForm' and 'StaffRequestFeatureForm' forms.
    I will be shortening the names for typing purposes to
    RB, RF, SRB and SRF.
    """
    def setUp(self):
        self.user = User.objects.create(
            username="user", email="user@example.com", password="password")
        self.user.save()

    def test_submitting_forms_without_title_or_description_displays_correct_error_messages(self):
        rb = ReportBugForm(
            {'created_by': self.user, 'title': '', 'description': ''})
        rf = ReportBugForm(
            {'created_by': self.user, 'title': '', 'description': ''})
        srb = ReportBugForm(
            {'created_by': self.user, 'title': '', 'description': ''})
        srf = ReportBugForm(
            {'created_by': self.user, 'title': '', 'description': ''})
        self.assertFalse(rb.is_valid())
        self.assertFalse(rf.is_valid())
        self.assertFalse(srb.is_valid())
        self.assertFalse(srf.is_valid())
        self.assertEqual(rb.errors['title'], [u'This field is required.'])
        self.assertEqual(
            rb.errors['description'], [u'This field is required.'])
        self.assertEqual(rf.errors['title'], [u'This field is required.'])
        self.assertEqual(
            rf.errors['description'], [u'This field is required.'])
        self.assertEqual(srb.errors['title'], [u'This field is required.'])
        self.assertEqual(
            srb.errors['description'], [u'This field is required.'])
        self.assertEqual(srf.errors['title'], [u'This field is required.'])
        self.assertEqual(
            srf.errors['description'], [u'This field is required.'])

    def test_can_submit_post_without_url(self):
        rb = ReportBugForm({
            'created_by': self.user, 'title': 'title',
            'description': 'description', 'url': ''})
        rf = ReportBugForm({
            'created_by': self.user, 'title': 'title',
            'description': 'description', 'url': ''})
        srb = ReportBugForm({
            'created_by': self.user, 'title': 'title',
            'description': 'description', 'url': ''})
        srf = ReportBugForm({
            'created_by': self.user, 'title': 'title',
            'description': 'description', 'url': ''})
        self.assertTrue(rb.is_valid())
        self.assertTrue(rf.is_valid())
        self.assertTrue(srb.is_valid())
        self.assertTrue(srf.is_valid())
