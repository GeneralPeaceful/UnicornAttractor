from django import forms
from .models import Ticket

class ReportBugForm(forms.ModelForm):
    """
    Form to report a bug
    """
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'url')

class RequestFeatureForm(forms.ModelForm):
    """
    Form to request a feature
    """
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'url', 'price')