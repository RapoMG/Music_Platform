# Domain Model

## Core Catalog

### Artist

Represents a musical artist.

Key fields:
- `name`
- `description`
- `image`

Relationships:
- one artist has many albums

### Album

Represents an album released by an artist.

Key fields:
- `artist`
- `title`
- `cover`
- `release_date`
- `published`

Relationships:
- belongs to one artist
- has many songs
- has many genres through a many-to-many relation

### Song

Represents a track on an album.

Key fields:
- `album`
- `title`
- `track_no`
- `file`
- `length`
- `lyrics`
- `author`

Rules:
- track number must be unique within an album
- songs are ordered by `track_no`

### Genre

Represents a music genre assigned to albums.

Key fields:
- `name`

## Consumer Features

### ConsumerProfile

Extends the user with public profile information.

Key fields:
- `user`
- `avatar`
- `description`
- `created_at`
- `updated_at`

Relationship:
- one user has one consumer profile

### LibraryItem

Represents ownership or saved access to a song in a user library.

Key fields:
- `user`
- `song`
- `added_at`

Rules:
- a user cannot own the same song twice
- newest library items are listed first

### Playlist

Represents a user-created playlist.

Key fields:
- `user`
- `name`
- `description`
- `is_public`
- `created_at`
- `updated_at`

### PlaylistItem

Represents a song inside a playlist.

Key fields:
- `playlist`
- `song`
- `position`
- `added_at`

Why it matters:
- this is the through-style model that stores song order in a playlist
- ordering is explicit and queryable

Rules:
- position must be unique within a playlist
- items are ordered by `position`

## Relationship Summary

```text
User
|-- 1:1 ConsumerProfile
|-- 1:N LibraryItem
`-- 1:N Playlist

Artist
`-- 1:N Album

Album
|-- N:1 Artist
|-- 1:N Song
`-- N:M Genre

Playlist
`-- 1:N PlaylistItem

PlaylistItem
|-- N:1 Playlist
`-- N:1 Song

LibraryItem
|-- N:1 User
`-- N:1 Song
```

## Important Design Detail

The playlist feature is intentionally modeled with `PlaylistItem` instead of a plain `ManyToManyField`. That allows the application to store and reorder playlist positions cleanly.
