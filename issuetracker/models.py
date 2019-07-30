from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    """
    Model for both bug reports and feature requests, all summed up as a 'Ticket'
    """
    ticket_types = (
        ('Bug','Bug Report'),
        ('Feature','Feature Request')
    )
    ticket_status = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Complete', 'Complete')
    )
    
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=250)
    description = models.TextField()
    url = models.CharField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=20.00)
    ticket_type = models.CharField(max_length=20, choices=ticket_types, blank=False)
    status = models.CharField(max_length=20, choices=ticket_status, default='Pending')
    created_on = models.DateTimeField(default=datetime.now)
    completion = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Vote(models.Model):
    """
    Model for handling users' votes on tickets
    """
    voted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING)
    voted_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username

class Contribution(models.Model):
    """
    Model for tracking contributions made towards feature development
    """

    contributor = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=5, decimal_places=2, blank=False)
    contributed_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.userid.username
