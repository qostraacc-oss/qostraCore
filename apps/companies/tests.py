from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.workspaces.models import Workspace
from apps.companies.models import Company

User = get_user_model()

class CompanyModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword123")
        self.workspace = Workspace.objects.create(
            owner=self.user,
            name="Test Workspace",
            slug="test-workspace"
        )

    def test_company_creation(self):
        company = Company.objects.create(
            workspace=self.workspace,
            name="Acme Corporation"
        )
        self.assertEqual(company.name, "Acme Corporation")
        self.assertEqual(company.workspace, self.workspace)
        self.assertEqual(str(company), "Acme Corporation")
