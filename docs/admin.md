# Admin

## Purpose

The Django admin is part of the project requirements and acts as the internal content management interface for catalog data.

## Current State

### Catalog admin

`apps.catalog.admin` currently includes:
- `ArtistAdmin`
- `AlbumAdmin`
- `GenreAdmin`
- inline editing for albums under artists
- inline editing for songs under albums
- search and filters on albums
- custom preview rendering for album covers
- computed columns such as song counts and genre names

### Consumers admin

`apps.consumers.admin` is currently empty.

That means consumer-related models such as profiles, playlists, playlist items, and library items are not yet manageable from the admin panel.

## Recommended Next Improvements

- register `ConsumerProfile`, `Playlist`, `PlaylistItem`, and `LibraryItem`
- add `search_fields` for username and playlist name
- add `list_filter` for public/private playlists and dates
- use `select_related`-friendly list views where helpful

## Documentation Rule

Whenever admin behavior changes, document:
- which models are manageable,
- which filters/search tools exist,
- any custom display logic worth knowing.
