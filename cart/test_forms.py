import datetime
from django.test import TestCase
from .forms import MakePaymentForm

class TestMakePaymentForm(TestCase):
    """
    Runs tests against the 'MakePaymentForm' form
    """
    def test_all_fields_required_and_display_correct_error_messages(self):
        form = MakePaymentForm({"card_number": '', "cvv": '', "expiry_month": '', "expiry_year": ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['card_number'], [u'This field is required.'])
        self.assertEqual(form.errors['cvv'], [u'This field is required.'])
        self.assertEqual(form.errors['expiry_year'], [u'This field is required.'])
        self.assertEqual(form.errors['expiry_month'], [u'This field is required.'])
    
    def test_month_and_year_choices_are_in_specific_range(self):
        form1 = MakePaymentForm({"card_number": '4242424242424242', "cvv": '222', "expiry_month": 0, "expiry_year": datetime.date.today().year-1})
        form2 = MakePaymentForm({"card_number": '4242424242424242', "cvv": '222', "expiry_month": 1, "expiry_year": datetime.date.today().year})
        form3 = MakePaymentForm({"card_number": '4242424242424242', "cvv": '222', "expiry_month": 12, "expiry_year": datetime.date.today().year+10})
        form4 = MakePaymentForm({"card_number": '4242424242424242', "cvv": '222', "expiry_month": 13, "expiry_year": datetime.date.today().year+11})
        self.assertNotIn(form1['expiry_month'].value(), range(1, 13))
        self.assertNotIn(form1['expiry_year'].value(), range(datetime.date.today().year, datetime.date.today().year+11))
        self.assertIn(form2['expiry_month'].value(), range(1, 13))
        self.assertIn(form2['expiry_year'].value(), range(datetime.date.today().year, datetime.date.today().year+11))
        self.assertIn(form3['expiry_month'].value(), range(1, 13))
        self.assertIn(form3['expiry_year'].value(), range(datetime.date.today().year, datetime.date.today().year+11))
        self.assertNotIn(form4['expiry_month'].value(), range(1, 13))
        self.assertNotIn(form4['expiry_year'].value(), range(datetime.date.today().year, datetime.date.today().year+11))