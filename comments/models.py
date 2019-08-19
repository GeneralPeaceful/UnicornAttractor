from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from issuetracker.models import Ticket
from posts.models import Post

class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ticket = models.ForeignKey(Ticket, blank=True, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    posted_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username+" commented on "+str(self.posted_on.date().strftime("%d-%m-%Y"))+" the comment: "+self.comment