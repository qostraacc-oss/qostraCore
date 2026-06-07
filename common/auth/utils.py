from common.auth.core import GenericJWTAuthentication
from common.auth.user_sync import core_user_sync_service

class WorkspaceJWTAuthentication(GenericJWTAuthentication):
    """
    Workspace-specific JWT Authentication.
    Uses CoreUserSyncService to handle user registration/caching.
    """
    @property
    def sync_service(self):
        return core_user_sync_service

# For backward compatibility and reference
JWTAuthentication = WorkspaceJWTAuthentication

