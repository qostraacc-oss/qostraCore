# Project Structure

## Project Overview
**QostraCore** manages the multi-tenant scaffolding and role-based access control (RBAC) definitions for the Qostra ERP platform. It resolves organization/company hierarchy structures, configures isolated workspace workspaces, structures project team profiles, and maps users to role permissions. It serves as the primary authorization boundary for resource queries.

This document provides a detailed overview of the QostraCore project directory structure and the purpose of each component.

## Root Directory
- `/apps/`: Contains custom Django applications (the core tenant and workspace structure).
- `/common/`: Central shared exceptions, utilities, middleware, and base permissions.
- `/config/`: Main project settings, routing, and wsgi/asgi entry points.
- `manage.py`: Django command-line utility.
- `pyproject.toml` / `uv.lock`: Dependency configuration managed by `uv`.

## 1. Apps (`/apps/`)
Logic is modularized into separate apps based on business entities.

### Workspaces (`/workspaces/`)
Manages workspaces (the high-level logical containers for team members and projects).
- `models.py`: Defines the custom `User` model (with UUID primary key), `Workspace` model, and its membership associations.
- `views/`: Package managing workspace views.
- `serializers/`: Handles workspace request and response schemas.
- `services/`: Encapsulates workspace business services.

### Companies (`/companies/`)
Manages organizational structure at the company level.
- `models.py`: Defines the `Company` model (parent entity of workspaces/teams).
- `views/`: Package managing company views.
- `serializers/`: Handles company data validation.
- `services/`: Encapsulates company business services.

### Teams (`/teams/`)
Manages teams within workspaces.
- `models.py`: Defines `Team` models and associations with workspaces.
- `views/`: Package managing team views.
- `serializers/`: Handles team data validation.
- `services/`: Encapsulates team business services.

### Roles & Permissions (`/roles/` & `/permissions/`)
Handles role-based access control (RBAC) definitions and permission checks.
- `models.py`: Custom role and permission models.
- `views/`: Packages managing role and permission views.
- `serializers/`: Handles RBAC data validation.
- `services/`: Encapsulates RBAC business services.

## 2. Common Components (`/common/`)
- `auth/`: Centralized authentication core logic and workspace utils.
- `middleware/`: Workspace context resolving middleware (e.g., extracting active workspace ID from requests).
- `permissions/`: Common decorators and class-based permissions to enforce workspace-level authorization.
- `exceptions/`: Core custom exception handlers.

## 3. Configuration (`/config/`)
- `settings/`: Multi-environment settings structure (`base.py`, `dev.py`, `prod.py`, `test.py`).

## 4. Documentation (`/.project/`)
- `project_rules.md`: Core developer rules and UV configurations.
- `project_structure.md`: This file.
- `api/`: Folder containing Markdown API documentation files for each application.
