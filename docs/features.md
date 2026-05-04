# Features

## Catalog Browsing

Users can:
- browse all artists,
- open an artist page to see published albums,
- open an album page to see songs and album metadata,
- browse genres,
- search artists, albums, songs, and users.

## Authentication

The project uses:
- Django authentication for the web UI,
- Djoser and JWT-related endpoints for the API,
- a custom user model with unique username and email.

## Profiles

Users have public profiles with:
- avatar,
- description,
- public playlists,
- a grouped library display.

Owners can also:
- edit profile details,
- update account fields,
- change password.

## Library

Authenticated users can:
- add a song to their library,
- add an entire album to their library,
- view their saved library via the API.

The home page also uses library activity to surface recent and trending content.

## Playlists

Authenticated users can:
- create playlists,
- edit playlist metadata,
- add songs,
- remove songs,
- reorder songs,
- choose whether a playlist is public.

Public behavior:
- public playlists are visible on profile pages,
- public playlist details can be retrieved through the API.

Private behavior:
- playlist edit routes are owner-only,
- private playlist API access is restricted to the owner.

## Admin and Seed Data

The project includes:
- custom admin configuration for catalog data,
- a `seed_catalog` command for generating realistic sample artists, albums, songs, and genres.
