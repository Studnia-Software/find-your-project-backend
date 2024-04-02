from django.db import models


class UserDetails(models.Model):
    description = models.TextField(max_length=2047, blank=True)
