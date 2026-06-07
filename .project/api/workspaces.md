# Workspaces API Reference

Workspaces represent the high-level logical tenants/containers for teams, roles, permissions, and companies.

## Table of Contents
- [Authentication](#authentication)
- [1. Onboarding Workspace API](#1-onboarding-workspace-api)
  - [A. Create Onboarding Workspace](#a-create-onboarding-workspace)
- [2. Multi-Workspace Management API](#2-multi-workspace-management-api)
  - [A. List Workspaces](#a-list-workspaces)
  - [B. Create Workspace (Manage)](#b-create-workspace-manage)
  - [C. Get Workspace Details](#c-get-workspace-details)
  - [D. Update Workspace](#d-update-workspace)
  - [E. Delete Workspace](#e-delete-workspace)
- [3. Workspace Members API](#3-workspace-members-api)
  - [A. List Workspace Members](#a-list-workspace-members)

---

## Authentication
All requests must include the JWT bearer token in the headers:
```http
Authorization: Bearer <jwt_access_token>
```

---

## 1. Onboarding Workspace API

This endpoint is used during user onboarding to create the initial workspace. It enforces a restriction limiting each user to a single workspace.

* **Endpoints**: 
  * `/workspaces/onboarding/` (Create Only)

### A. Create Onboarding Workspace
Creates a new onboarding workspace. Only allowed if the user does not already own a workspace.

> [!NOTE]
> Creating a workspace automatically registers a `WorkspaceMember` record linking the creator (`owner`) to the workspace with the `owner` role.

* **Method**: `POST`
* **Request Payload**:
```json
{
  "name": "My Business Workspace",
  "slug": "my-business-workspace",
  "type": "business",             // Choice: "individual" or "business" (Required)
  "company_name": "My Company Name", // Optional (write-only, for business type; defaults to workspace name)
  "company_size": "10-50",        // Optional (write-only, for business type)
  "industry": "Technology"        // Optional (write-only, for business type)
}
```
* **Success Response Example (201 Created)**:
```json
{
    "id": "aa89fbd8-752b-4339-a2e8-d7ad7f3a1b4c",
    "owner": "1ea795e3-915c-45b7-8c7f-1365df199d30",
    "name": "My Business Workspace",
    "slug": "my-business-workspace211",
    "is_active": true,
    "companies": [
        {
            "id": "7198c847-232c-41cd-8104-1203fa105bc2",
            "name": "My Business Workspace",
            "company_size": "10-50",
            "industry": "Technology",
            "created_at": "2026-06-06T06:29:28.675633Z",
            "updated_at": "2026-06-06T06:29:28.675633Z"
        }
    ],
    "created_at": "2026-06-06T06:29:28.647474Z",
    "updated_at": "2026-06-06T06:29:28.647474Z"
}
```
* **Error Response Example (400 Bad Request)**:
```json
{
  "non_field_errors": [
    "Onboarding already completed. A default workspace has already been created for this account."
  ]
}
```

---

## 2. Multi-Workspace Management API

These endpoints allow users to create and manage multiple workspaces over separate requests without any onboarding validation limits.

* **Endpoints**: 
  * `/workspaces/manage/` (List / Create)
  * `/workspaces/manage/<uuid:pk>/` (Detail / Update / Delete)

### A. List Workspaces
Lists all workspaces owned by the authenticated user.

* **Method**: `GET`
* **Success Response Example (200 OK)**:
```json
[
  {
    "id": "18f50ad9-1cfd-4d76-bc3f-723a101ef2a3",
    "owner": "1ea795e3-915c-45b7-8c7f-1365df199d30",
    "name": "My Business Workspace",
    "slug": "my-business-workspace",
    "is_active": true,
    "companies": [
      {
        "id": "b96f2e2d-34e8-4034-be57-9d7a9b0c20ab",
        "name": "My Business Workspace",
        "company_size": "10-50",
        "industry": "Technology",
        "created_at": "2026-06-05T09:29:51.014Z",
        "updated_at": "2026-06-05T09:29:51.014Z"
      }
    ],
    "created_at": "2026-06-05T09:29:51.002Z",
    "updated_at": "2026-06-05T09:29:51.002Z"
  }
]
```

### B. Create Workspace (Manage)
Creates a new workspace for the authenticated user, allowing multiple workspaces.

> [!NOTE]
> Creating a workspace automatically registers a `WorkspaceMember` record linking the creator (`owner`) to the workspace with the `owner` role.

> [!WARNING]
> The authenticated user **must have completed onboarding** (owns at least one workspace created via the onboarding endpoint) before managing or creating workspaces here. If onboarding is not completed, this endpoint returns a `400 Bad Request` validation error.

* **Method**: `POST`
* **Request Payload**: Same format as Onboarding Workspace creation.
* **Success Response Example (201 Created)**:
```json
{
  "id": "2af50ad9-1cfd-4d76-bc3f-723a101ef2a3",
  "name": "Another Workspace",
  "slug": "another-workspace"
}
```

### C. Get Workspace Details
Retrieves details of a specific workspace owned by the user.

* **Method**: `GET`
* **Success Response Example (200 OK)**:
```json
{
  "id": "18f50ad9-1cfd-4d76-bc3f-723a101ef2a3",
  "owner": "1ea795e3-915c-45b7-8c7f-1365df199d30",
  "name": "My Business Workspace",
  "slug": "my-business-workspace",
  "is_active": true,
  "companies": [
    {
      "id": "b96f2e2d-34e8-4034-be57-9d7a9b0c20ab",
      "name": "My Business Workspace",
      "company_size": "10-50",
      "industry": "Technology",
      "created_at": "2026-06-05T09:29:51.014Z",
      "updated_at": "2026-06-05T09:29:51.014Z"
    }
  ],
  "created_at": "2026-06-05T09:29:51.002Z",
  "updated_at": "2026-06-05T09:29:51.002Z"
}
```

### D. Update Workspace
Updates a workspace owned by the user. Supports nested updates of the associated company details.

* **Method**: `PUT` or `PATCH`
* **Request Payload (PATCH example for workspace details)**:
```json
{
  "name": "New Workspace Name"
}
```
* **Request Payload (PATCH example using flat company fields)**:
You can pass the company properties directly at the root level of the payload (matching the structure used during creation):
```json
{
  "company_name": "Flat Updated Company Name Ltd",
  "company_size": "250-500",
  "industry": "Flat Updated Industry"
}
```
* **Success Response (200 OK)**: Returns the updated workspace object.

### E. Delete Workspace
Deletes a workspace owned by the user.

* **Method**: `DELETE`
* **Success Response (204 No Content)**

---

## 3. Workspace Members API

These endpoints allow users to list members belonging to a workspace.

* **Endpoints**:
  * `/workspaces/<uuid:workspace_id>/members/` (List Only)

### A. List Workspace Members
Retrieves all users/members belonging to the specified workspace ID. The requesting user must be an active member of this workspace.

* **Method**: `GET`
* **Success Response Example (200 OK)**:
```json
[
  {
    "id": "da89fbd8-752b-4339-a2e8-d7ad7f3a1b4c",
    "workspace": "aa89fbd8-752b-4339-a2e8-d7ad7f3a1b4c",
    "user": {
      "id": "anfique",
      "username": "anfique",
      "email": "anfique@qostra.com",
      "first_name": "Anfique",
      "last_name": "Rahman"
    },
    "role": "owner",
    "joined_at": "2026-06-06T06:29:28.675633Z",
    "updated_at": "2026-06-06T06:29:28.675633Z"
  },
  {
    "id": "eb89fbd8-752b-4339-a2e8-d7ad7f3a1b4d",
    "workspace": "aa89fbd8-752b-4339-a2e8-d7ad7f3a1b4c",
    "user": {
      "id": "akhil",
      "username": "akhil",
      "email": "akhil@qostra.com",
      "first_name": "Akhil",
      "last_name": "P"
    },
    "role": "member",
    "joined_at": "2026-06-06T07:12:00.000000Z",
    "updated_at": "2026-06-06T07:12:00.000000Z"
  }
]
```

* **Error Response Example (403 Forbidden)**:
```json
{
  "detail": "You do not have permission to view this workspace's members."
}
```

