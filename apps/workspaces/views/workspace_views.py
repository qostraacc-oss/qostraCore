from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.workspaces.models import Workspace, WorkspaceMember
from apps.workspaces.serializers import (
    WorkspaceSerializer,
    WorkspaceCreateSerializer,
    WorkspaceManageSerializer,
    WorkspaceManageCreateSerializer,
    WorkspaceMemberSerializer,
)


class WorkspaceOnboardingAPIView(APIView):
    """
    APIView to create the initial onboarding workspace.
    Enforces a limit of one workspace per user via WorkspaceCreateSerializer.
    Only allows POST requests.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = WorkspaceCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            workspace = serializer.save()
            return Response(
                WorkspaceSerializer(workspace).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkspaceManageListCreateAPIView(APIView):
    """
    APIView to list and create workspaces.
    Does not restrict the user to a single workspace.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        workspaces = Workspace.objects.filter(owner=request.user)
        serializer = WorkspaceManageSerializer(workspaces, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkspaceManageCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            workspace = serializer.save()
            return Response(
                WorkspaceManageSerializer(workspace).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkspaceManageDetailAPIView(APIView):
    """
    APIView to retrieve, update (PUT/PATCH), and delete workspaces.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Workspace, pk=pk, owner=user)

    def get(self, request, pk):
        workspace = self.get_object(pk, request.user)
        serializer = WorkspaceManageSerializer(workspace)
        return Response(serializer.data)

    def put(self, request, pk):
        workspace = self.get_object(pk, request.user)
        serializer = WorkspaceManageSerializer(
            workspace, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        workspace = self.get_object(pk, request.user)
        serializer = WorkspaceManageSerializer(
            workspace, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        workspace = self.get_object(pk, request.user)
        workspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkspaceMemberListAPIView(APIView):
    """
    APIView to list all workspace users under the workspace ID.
    The requesting user must be a member of the workspace.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, workspace_id):
        workspace = get_object_or_404(Workspace, id=workspace_id)
        
        # Enforce membership check
        if not WorkspaceMember.objects.filter(workspace=workspace, user=request.user).exists():
            return Response(
                {"detail": "You do not have permission to view this workspace's members."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        members = WorkspaceMember.objects.filter(workspace=workspace).select_related('user')
        serializer = WorkspaceMemberSerializer(members, many=True)
        return Response(serializer.data)

