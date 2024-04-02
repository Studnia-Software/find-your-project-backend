from django.db import models
from django.conf import settings

from api.models.project import Project
from .project_roles import ProjectRole


class ProjectMemberRelation(models.Model):
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    project_role_id = models.ForeignKey(to=ProjectRole, on_delete=models.SET_NULL, null=True)
