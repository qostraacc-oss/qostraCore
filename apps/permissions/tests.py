from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.workspaces.models import Workspace
from apps.permissions.models import Permission

User = get_user_model()

class PermissionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword123")
        self.workspace = Workspace.objects.create(
            owner=self.user,
            name="Test Workspace",
            slug="test-workspace"
        )

    def test_permission_creation(self):
        perm = Permission.objects.create(
            workspace=self.workspace,
            name="Manage Users",
            codename="manage_users",
            description="Allows managing users"
        )
        self.assertEqual(perm.codename, "manage_users")
        self.assertEqual(perm.workspace, self.workspace)
        self.assertEqual(str(perm), "manage_users (Test Workspace)")
