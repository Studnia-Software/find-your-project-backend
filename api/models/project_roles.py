from django.db import models


class ProjectRole(models.Model):
    name = models.TextField(max_length=255)
