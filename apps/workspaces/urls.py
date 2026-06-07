from django.urls import path
from apps.workspaces.views import (
    WorkspaceOnboardingAPIView,
    WorkspaceManageListCreateAPIView,
    WorkspaceManageDetailAPIView,
    WorkspaceMemberListAPIView,
)

urlpatterns = [
    path("onboarding/", WorkspaceOnboardingAPIView.as_view(), name="workspace-onboarding"),
    path("manage/",WorkspaceManageListCreateAPIView.as_view(),name="workspace-manage-list"),
    path("manage/<uuid:pk>/",WorkspaceManageDetailAPIView.as_view(),name="workspace-manage-detail",),
    path("<uuid:workspace_id>/members/", WorkspaceMemberListAPIView.as_view(), name="workspace-members-list"),
]
