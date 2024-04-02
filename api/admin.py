from django.contrib import admin
from . import models

admin.site.register(models.project.Project)
admin.site.register(models.project.ProjectRole)
admin.site.register(models.project.ProjectMemberRelation)
admin.site.register(models.project.ProjectDetails)

