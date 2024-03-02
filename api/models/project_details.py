from django.db import models


class ProjectDetails(models.Model):
    title = models.TextField(max_length=255)
