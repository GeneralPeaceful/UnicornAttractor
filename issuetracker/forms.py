from django import forms
from .models import Ticket

class ReportBugForm(forms.ModelForm):
    """
    Form to report a bug
    """
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'url')


class StaffReportBugForm(forms.ModelForm):
    """
    Form to report a bug
    """
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'url', 'status', 'status_colour')


class RequestFeatureForm(forms.ModelForm):
    """
    Form to request a feature
    """
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'url')


class StaffRequestFeatureForm(forms.ModelForm):
    """
    Form to report a bug
    """
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'url', 'price', 'status', 'status_colour')