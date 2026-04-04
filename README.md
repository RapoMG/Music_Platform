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
│  │  ├─ music/
│  │  ├─ playlists/
│  │  ├─ purchases/
│  │  └─ library/
│  ├─ media/
│  ├─ static/
│  └─ templates/
├─ frontend/
└─ scripts/
