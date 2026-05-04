# Documentation Index

This folder is the main documentation home for the project.

## Start Here

- `setup.md` - how to run the project locally with or without Docker
- `architecture.md` - how the repository is organized
- `domain-model.md` - the main entities and relationships
- `features.md` - the core user journeys implemented today
- `api.md` - API surface overview
- `commands.md` - frequently used management and Docker commands
- `testing.md` - what is tested and how to run tests
- `admin.md` - current Django admin customizations
- `decisions/` - short architecture decision records

## Documentation Style

This project uses a docs-as-code approach:
- docs live in the repository,
- Markdown is the source of truth for narrative documentation,
- technical behavior should be documented close to the code when practical,
- high-churn details should be generated or kept brief to reduce drift.

## Maintenance Rule

When a feature changes, update:
1. the code,
2. the most relevant page in `docs/`,
3. the `README.md` only if setup or project scope changed.
