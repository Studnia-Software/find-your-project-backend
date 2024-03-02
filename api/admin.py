from django.contrib import admin
from . import models

admin.site.register(models.Project)
admin.site.register(models.ProjectRole)
admin.site.register(models.ProjectMemberRelation)
admin.site.register(models.ProjectDetails)

