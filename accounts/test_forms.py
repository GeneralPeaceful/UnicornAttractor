from django.test import TestCase
from .forms import UserLoginForm, UserRegistrationForm

class TestUserForms(TestCase):
    """
    Runs tests against the 'UserLoginForm' and 'UserRegistrationForm' forms
    """
    def test_user_login_requires_username_and_password_to_be_valid(self):
        form1 = UserLoginForm({'username': '', 'password': 'password'})
        form2 = UserLoginForm({'username': 'user', 'password': ''})
        form3 = UserLoginForm({'username': 'user', 'password': 'password'})
        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())
        self.assertTrue(form3.is_valid())
    
    def test_user_login_displays_correct_messages_for_missing_fields(self):
        form = UserLoginForm({'username': '', 'password': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [u'This field is required.'])
        self.assertEqual(form.errors['password'], [u'This field is required.'])
    
    def test_user_registration_requires_all_fields(self):
        form = UserRegistrationForm({'username': '', 'password1': '', 'password2': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [u'This field is required.'])
        self.assertEqual(form.errors['password1'], [u'This field is required.'])
        self.assertEqual(form.errors['password2'], [u'This field is required.'])
    
    def test_passwords_on_user_registration_must_be_the_same(self):
        form_true = UserRegistrationForm({'username': 'username1', 'email': 'user1@example.com', 'password1': 'matching password', 'password2': 'matching password'})
        form_false = UserRegistrationForm({'username': 'username2', 'email': 'user2@example.com', 'password1': 'matching password', 'password2': 'not matching password'})
        self.assertTrue(form_true.is_valid())
        self.assertFalse(form_false.is_valid())