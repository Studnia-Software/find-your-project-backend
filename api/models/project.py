from django.db import models
from .project_details import ProjectDetails


class Project(models.Model):
    project_details_id = models.ForeignKey(to=ProjectDetails, on_delete=models.SET_NULL, null=True)
