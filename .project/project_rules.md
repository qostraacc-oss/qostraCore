# Project Rules

This document outlines the core development rules and best practices for the QostraCore project. All developers and AI agents MUST adhere to these rules.

> [!IMPORTANT]
> **AI AGENT DIRECTIVE**: Any AI agent interacting with this codebase MUST read both `project_rules.md` and `project_structure.md` before making any changes or analysis.

## 1. Core Structural Rules
- **Localized Logic**: Keep logic app-specific unless it is shared across multiple domains.
- **Shared Utilities**: Only place elements that cross-cut domains (e.g., workspace resolution middleware) in the `common/` directory.
- **Package Organization**: Organize views and other complex app components into sub-packages rather than single large files.

## 2. Multi-Tenancy and Workspace Scoping
- **Workspace Isolation**: All database queries for workspace-related resources MUST explicitly filter by the active workspace or tenant ID (typically resolved via middleware or request params).
- **Membership Checks**: Ensure a user belongs to a workspace before letting them perform read/write actions in it.
- **Fail Closed**: Permissions and middleware must default to denying access if the workspace context cannot be verified.

## 3. User Identity and Authentication
- **Custom User Model**: All microservices must use a custom User model where the primary key `id` is a `UUIDField` mapping directly to the `user_id` from the QostraAuth service.
- **No Local IDs Exposed**: Avoid using or exposing local integer-based IDs for users in APIs, serialization, or internal messaging.
- **User Synchronization**: Local user tables should be synchronized from JWT token claims or webhook events, storing only the necessary profile data.

## 3. Code Quality and Maintenance
- **Consistency**: Follow established patterns for views, serializers, and services.
- **Clear Imports**: Use clean, package-level imports rather than nested relative imports.
- **No Leftovers**: Clean up old files and imports when refactoring code.

## 4. Scalability and Optimization
- **Eager Loading**: Prevent N+1 queries by using `select_related` and `prefetch_related` inside managers and serializers.
- **Documentation**: Keep project rules and structure docs updated as structures change.
  - **API Documentation**: Whenever a route is modified, added, or a request/response schema is changed, the corresponding API document inside `.project/api/` MUST be updated immediately. Each API markdown file MUST include a Table of Contents (index) at the top of the file for quick navigation.

## 5. Deployment and Environment
- **Security Check**: Always run `python manage.py check --deploy` before production rollouts.
- **Dependency Management**: Use `uv` for package management. Keep `pyproject.toml` and `uv.lock` updated, and avoid using raw `pip` commands.
  - Sync local environment: `uv sync`
  - Add dependency: `uv add <package>`
  - Remove dependency: `uv remove <package>`
  - Run Django commands: `uv run python manage.py <command>`
