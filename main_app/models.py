from django.db import models
from django.contrib.auth.models import User
# create first model
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    