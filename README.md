# Music Platform API

Backend application for a music platform built with **Django** and **Django REST Framework**.

The project is designed as an API-first service for a web application and future mobile client. It supports two main user roles:

- **Consumers** — can browse music, listen to tracks, create playlists, purchase tracks or albums, and download purchased content.
- **Creators** — can manage albums, tracks, covers, descriptions, pricing, genre tags, and tour-related information.

## Project status

This project is currently under active development.

Planned core features:
- user authentication and authorization
- consumer and creator roles
- album and track management
- playlist creation
- music purchases
- access to purchased content
- creator news and tour information
- recommendation-oriented metadata such as genres and tags

## Tech stack

- **Python**
- **Django**
- **Django REST Framework**
- **PostgreSQL**
- **Docker**
- **Git**

Planned or possible additions:
- JWT authentication
- Nginx
- Celery
- Redis
- cloud media storage
- separate frontend client
- mobile application client

## Architecture overview

This repository is organized as an API backend with supporting project documentation and infrastructure configuration.

- `backend/` — Django REST Framework backend
- `docs/` — project documentation, architectural notes, diagrams, decisions
- `docker/` — Docker configuration
- `frontend/` — reserved for future frontend client
- `requirements/` — Python dependency files
- `scripts/` — helper scripts for local development

## Project structure

```text
music-platform/
├─ .gitignore
├─ .editorconfig
├─ README.md
├─ .env.example
├─ docker-compose.yml
├─ requirements/
│  ├─ base.txt
│  ├─ dev.txt
│  └─ prod.txt
├─ docs/
├─ docker/
├─ backend/
│  ├─ manage.py
│  ├─ config/
│  │  └─ settings/
│  │     ├─ base.py
│  │     ├─ dev.py
│  │     └─ prod.py
│  ├─ apps/
│  │  ├─ common/
│  │  ├─ users/
│  │  ├─ creators/
│  │  ├─ consumers/
│  │  └─ *purchases/
│  ├─ media/
│  │  ├─ albums/
│  │  ├─ artists/
│  │  └─ songs/
│  ├─ static/
│  └─ templates/
├─ frontend/
└─ scripts/
```

## API endpoints

Base API prefix: `/api/`

Authentication (Djoser + JWT):
- `/api/auth/` endpoints from `djoser.urls`
- `/api/auth/` JWT endpoints from `djoser.urls.jwt`

### Catalog (router)

The following resources are registered with DRF `DefaultRouter` and expose standard actions:
- `GET /api/artists/`, `POST /api/artists/`, `GET /api/artists/{id}/`, `PUT/PATCH/DELETE /api/artists/{id}/`
- `GET /api/albums/`, `POST /api/albums/`, `GET /api/albums/{id}/`, `PUT/PATCH/DELETE /api/albums/{id}/`
- `GET /api/songs/`, `POST /api/songs/`, `GET /api/songs/{id}/`, `PUT/PATCH/DELETE /api/songs/{id}/`
- `GET /api/genres/`, `POST /api/genres/`, `GET /api/genres/{id}/`, `PUT/PATCH/DELETE /api/genres/{id}/`

### Consumers

Public:
- `GET /api/consumers/profile/{user_id}/`
- `GET /api/users/{username}/playlists/`
- `GET /api/playlists/{id}/`

Authenticated (`IsAuthenticated`):
- `GET /api/consumers/library/`
- `POST /api/consumers/library/songs/{song_id}/add/`
- `POST /api/consumers/library/albums/{album_id}/add/`

### My playlists (router)

Registered with `DefaultRouter` as `me/playlists`.

Playlist CRUD:
- `GET /api/me/playlists/`
- `POST /api/me/playlists/`
- `GET /api/me/playlists/{id}/`
- `PUT /api/me/playlists/{id}/`
- `PATCH /api/me/playlists/{id}/`
- `DELETE /api/me/playlists/{id}/`

APlayer data:
- `GET /api/me/playlists/{id}/player/`
- Returns a list of playlist items formatted for APlayer (`name`, `artist`, `url`, `lrc`, `cover`, `position`).

Playlist items:
- `POST /api/me/playlists/{playlist_id}/items/add/`
  Request body:
  ```json
  { "song_id": 123 }
  ```
- `DELETE /api/me/playlists/{playlist_id}/items/{item_id}/remove/`
- `PATCH /api/me/playlists/{playlist_id}/items/{item_id}/reorder/`
  Request body:
  ```json
  { "position": 2 }
  ```

Temporary test page:
- `GET /api/player/` (server-rendered test page for APlayer)
