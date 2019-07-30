from django.contrib import admin
from .models import Ticket, Vote, Contribution

admin.site.register(Ticket)
admin.site.register(Vote)
admin.site.register(Contribution)