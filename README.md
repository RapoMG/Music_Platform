# OpenChord

OpenChord is a Django music platform centered on browsing artists and albums, managing personal libraries, and creating user playlists.

The repository contains both:
- a JSON API built with Django REST Framework,
- a server-rendered web UI built with Django templates.

## Current Scope

Implemented areas in the codebase include:
- custom user model with email and account type,
- authentication with Django auth, Djoser, and JWT support,
- catalog models for artists, albums, songs, and genres,
- public artist, album, genre, profile, and search pages,
- consumer profiles, libraries, and playlist management,
- seed data via a custom management command,
- Django admin customization,
- basic automated tests.

## Project Layout

```text
F:\Django_Final_Project
|-- backend/
|   |-- apps/
|   |   |-- catalog/
|   |   |-- consumers/
|   |   `-- users/
|   |-- config/
|   `-- manage.py
|-- docs/
|-- docker/
|-- frontend/
|-- notes/
`-- requirements/
```

## Quick Start

### Docker

```bash
docker compose --env-file .env.dev up --build
```

### Local commands

All Django commands should be run from the `backend/` directory:

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Seed sample data

```bash
cd backend
python manage.py seed_catalog
```

## Documentation

Project documentation lives in `docs/`:
- `docs/index.md` - starting point
- `docs/setup.md` - local environment and commands
- `docs/architecture.md` - application structure
- `docs/domain-model.md` - key model relationships
- `docs/features.md` - user-facing functionality
- `docs/api.md` - API overview
- `docs/testing.md` - tests and test targets
- `docs/admin.md` - Django admin notes
- `docs/decisions/` - short architecture/design decisions

## Notes

This repository has evolved from an earlier API-first plan into a mixed web-and-API Django application. The documentation in `docs/` reflects the current codebase rather than older roadmap ideas.
