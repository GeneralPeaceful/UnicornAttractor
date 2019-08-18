from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    """
    Model for both bug reports and feature requests, all summed up as a 'Ticket'
    """
    PENDING = 'To do'
    DOING = 'In Progress'
    DONE = 'Complete'
    
    ticket_types = (
        ('Bug','Bug Report'),
        ('Feature','Feature Request')
    )
    ticket_status = (
        ('To do', PENDING),
        ('In Progress', DOING),
        ('Complete', DONE)
    )
    ticket_status_colour = (
        ('dark', PENDING),
        ('warning', DOING),
        ('success', DONE)
    )
    
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=250)
    description = models.TextField()
    url = models.CharField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=20.00)
    ticket_type = models.CharField(max_length=20, choices=ticket_types, blank=False)
    status = models.CharField(max_length=20, choices=ticket_status, default=PENDING)
    status_colour = models.CharField(max_length=20, choices=ticket_status_colour, default='dark')
    created_on = models.DateTimeField(default=datetime.now)
    completion = models.IntegerField(default=0)

    def __str__(self):
        return self.ticket_type+": "+self.title

class Vote(models.Model):
    """
    Model for handling users' votes on tickets
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING)
    voted_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username+" voted on Bug: '"+self.ticket.title+"' on "+str(self.voted_on.date().strftime("%d-%m-%Y"))

class Contribution(models.Model):
    """
    Model for tracking contributions made towards feature development
    """

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=5, decimal_places=2, blank=False)
    contributed_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username+" contributed £"+str(self.amount)+" to Feature: '"+self.ticket.title+"' on "+str(self.contributed_on.date().strftime("%d-%m-%Y"))
