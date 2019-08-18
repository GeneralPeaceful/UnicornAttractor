import datetime

from django import forms

class MakePaymentForm(forms.Form):
    MONTH_CHOICES = [(i, i) for i in range(1, 13)]
    YEAR_CHOICES = [(i, i) for i in range(datetime.date.today().year, datetime.date.today().year+11)]
    
    card_number = forms.CharField(label='Card number', required=True)
    cvv = forms.CharField(label='Security code (CVV)', required=True)
    expiry_month = forms.ChoiceField(label='Expiry Month', choices=MONTH_CHOICES, required=True)
    expiry_year = forms.ChoiceField(label='Expiry Year', choices=YEAR_CHOICES, required=True)
    stripe_id = forms.CharField(widget=forms.HiddenInput)