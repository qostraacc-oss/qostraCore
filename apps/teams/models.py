# import uuid
# from django.db import models

# class Team(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     workspace = models.ForeignKey(
#         'workspaces.Workspace',
#         on_delete=models.CASCADE,
#         related_name="teams"
#     )
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.name} ({self.workspace.name})"
