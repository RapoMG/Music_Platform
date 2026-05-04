# API Overview

## Scope

The API currently covers:
- authentication,
- catalog resources,
- consumer profiles,
- libraries,
- playlists,
- a small utility endpoint for trending songs.

## Authentication

Mounted under:

```text
/api/auth/
```

This project includes Djoser routes and JWT support in the URL configuration.

## Catalog Endpoints

Registered with DRF router:
- `/api/artists/`
- `/api/albums/`
- `/api/songs/`
- `/api/genres/`

These expose the standard router actions for list and detail operations.

## Consumer Endpoints

Examples:
- `GET /api/consumers/profile/<user_id>/`
- `GET /api/consumers/library/`
- `POST /api/consumers/library/songs/<song_id>/add/`
- `POST /api/consumers/library/albums/<album_id>/add/`

## Playlist Endpoints

Public:
- `GET /api/users/<username>/playlists/`
- `GET /api/playlists/<id>/`

Owner-only:
- `GET /api/me/playlists/`
- `POST /api/me/playlists/`
- `PATCH /api/me/playlists/<id>/`
- `DELETE /api/me/playlists/<id>/`
- `GET /api/me/playlists/<id>/player/`
- `POST /api/me/playlists/<playlist_id>/items/add/`
- `DELETE /api/me/playlists/<playlist_id>/items/<item_id>/remove/`
- `PATCH /api/me/playlists/<playlist_id>/items/<item_id>/reorder/`

## Utility Endpoint

- `GET /api/api/library/trending/`

Note:
The current path contains a duplicated `api` segment because the endpoint path itself includes `api/` while also being mounted under `/api/`. This should be cleaned up in code later if you want a neater public route.

## Documentation Strategy

Manual API docs in Markdown are useful for overview and examples, but endpoint-by-endpoint behavior will drift over time if maintained by hand.

Recommended next step:
- generate an OpenAPI schema from DRF,
- expose Swagger UI or ReDoc for live endpoint documentation,
- keep this page as the high-level guide instead of duplicating full endpoint details.
