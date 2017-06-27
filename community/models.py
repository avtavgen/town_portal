from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User)
    upvotes = models.ManyToManyField(User, related_name='votes')
    submitted_on = models.DateTimeField(auto_now_add=True, editable=False)


class Comment(models.Model):
    body = models.TextField()
    commented_on = models.ForeignKey(Post)
    in_reply_to = models.ForeignKey('self', null=True)
    commented_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
