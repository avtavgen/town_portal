from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides selfupdating
    ``created`` and ``modified`` fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(TimeStampedModel):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Suka(TimeStampedModel):
    name = models.CharField(max_length=80)
    body = models.TextField()
    slug = models.SlugField(max_length=250, unique=True)
    publish = models.DateTimeField(default=timezone.now)
