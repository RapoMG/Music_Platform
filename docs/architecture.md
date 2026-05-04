# Architecture

## Overview

This is a Django application with two delivery layers over the same domain:
- REST API endpoints for programmatic access
- server-rendered HTML pages for the browser UI

That makes the project best understood as a shared domain model with two interfaces instead of as a pure API backend.

## Main Apps

### `apps.catalog`

Owns the music catalog:
- `Artist`
- `Album`
- `Song`
- `Genre`

Also includes:
- DRF viewsets and serializers for catalog resources
- seed command for generating sample data
- admin registrations for catalog management
- tests for model and serializer behavior

### `apps.consumers`

Owns user-facing music consumption features:
- `ConsumerProfile`
- `LibraryItem`
- `Playlist`
- `PlaylistItem`

Also includes:
- DRF endpoints for library and playlist operations
- Django template views for profiles, artists, albums, search, and playlists
- forms and services for playlist and profile workflows

### `apps.users`

Owns authentication-related user customization:
- custom `User` model
- custom user manager
- authentication backend
- serializers and validators

## URL Structure

### Web UI

Mounted at `/` through `apps.consumers.web_urls`.

Examples:
- `/`
- `/artists/`
- `/albums/<id>/`
- `/profile/<username>/`
- `/playlists/<username>/`

### API

Mounted under `/api/`.

Examples:
- `/api/artists/`
- `/api/albums/`
- `/api/consumers/library/`
- `/api/me/playlists/`

Authentication routes from Djoser and JWT are mounted under:

```text
/api/auth/
```

## Templates and Static Assets

- templates: `frontend/templates/`
- static assets: `frontend/static/`
- bundled third-party player assets: `backend/static/player/`

## Current Architectural Character

The codebase is currently:
- monolithic Django rather than split into separate deployable services,
- shared-model oriented,
- fairly conventional in structure,
- moving toward cleaner separation via services and serializers, especially in playlist and library features.
