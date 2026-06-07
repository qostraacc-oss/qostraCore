from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.workspaces.models import Workspace, WorkspaceMember
from apps.companies.models import Company

User = get_user_model()

class CompanySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    
    class Meta:
        model = Company
        fields = ['id', 'name', 'company_size', 'industry', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class WorkspaceSerializer(serializers.ModelSerializer):
    companies = CompanySerializer(many=True, read_only=True)
    
    class Meta:
        model = Workspace
        fields = ['id', 'owner', 'name', 'slug', 'is_active', 'companies', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'is_active', 'created_at', 'updated_at']

class WorkspaceCreateSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=[('individual', 'Individual'), ('business', 'Business')],
        write_only=True
    )
    
    # Business-specific optional fields
    company_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=True,
        write_only=True
    )
    company_size = serializers.CharField(
        max_length=50, required=False, allow_blank=True, allow_null=True,
        write_only=True
    )
    industry = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True,
        write_only=True
    )
    
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'slug', 'type', 'company_name', 'company_size', 'industry']

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            # Enforce limit of one workspace per user
            if Workspace.objects.filter(owner=request.user).exists():
                raise serializers.ValidationError("Onboarding already completed. A default workspace has already been created for this account.")
        return attrs
        
    def create(self, validated_data):
        request = self.context.get('request')
        owner = request.user if request else None
        
        workspace_type = validated_data.pop('type')
        company_name = validated_data.pop('company_name', None)
        company_size = validated_data.pop('company_size', None)
        industry = validated_data.pop('industry', None)
        
        with transaction.atomic():
            # Create the Workspace
            workspace = Workspace.objects.create(
                owner=owner,
                **validated_data
            )
            
            # Auto-create the WorkspaceMember record with OWNER role
            if owner:
                WorkspaceMember.objects.create(
                    workspace=workspace,
                    user=owner,
                    role=WorkspaceMember.RoleChoices.OWNER
                )
            
            # If type is business, create a corresponding Company
            if workspace_type == 'business':
                Company.objects.create(
                    workspace=workspace,
                    name=company_name or workspace.name,  # Use custom company name if provided, fallback to workspace name
                    company_size=company_size,
                    industry=industry
                )
            
        return workspace


class WorkspaceManageSerializer(WorkspaceSerializer):
    # Allow flat company update fields at the root level (same structure as creation)
    company_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=True,
        write_only=True
    )
    company_size = serializers.CharField(
        max_length=50, required=False, allow_blank=True, allow_null=True,
        write_only=True
    )
    industry = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True,
        write_only=True
    )

    class Meta(WorkspaceSerializer.Meta):
        fields = WorkspaceSerializer.Meta.fields + ['company_name', 'company_size', 'industry']

    def update(self, instance, validated_data):
        # Extract flat company fields
        company_name = validated_data.pop('company_name', None)
        company_size = validated_data.pop('company_size', None)
        industry = validated_data.pop('industry', None)
        
        # Update workspace fields
        instance = super().update(instance, validated_data)
        
        # Update company details using flat root fields if provided
        if company_name is not None or company_size is not None or industry is not None:
            company = instance.companies.first()
            if company:
                if company_name is not None:
                    company.name = company_name
                if company_size is not None:
                    company.company_size = company_size
                if industry is not None:
                    company.industry = industry
                company.save()
            else:
                Company.objects.create(
                    workspace=instance,
                    name=company_name or instance.name,
                    company_size=company_size,
                    industry=industry
                )
        
        return instance


class WorkspaceManageCreateSerializer(WorkspaceCreateSerializer):
    """
    Serializer to create a workspace.
    Bypasses the single-workspace check to allow multiple workspaces,
    but ensures that the user has completed onboarding first.
    """
    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            if not Workspace.objects.filter(owner=request.user).exists():
                raise serializers.ValidationError(
                    "Onboarding must be completed before managing workspaces. "
                    "Please use the onboarding endpoint to create your first workspace."
                )
        return attrs


class UserMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class WorkspaceMemberSerializer(serializers.ModelSerializer):
    user = UserMinSerializer(read_only=True)
    
    class Meta:
        model = WorkspaceMember
        fields = ['id', 'workspace', 'user', 'role', 'joined_at', 'updated_at']
        read_only_fields = ['id', 'workspace', 'user', 'joined_at', 'updated_at']
