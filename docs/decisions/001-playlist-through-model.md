# ADR 001: Playlist Ordering Uses a Dedicated Item Model

## Status

Accepted

## Context

The project needs user playlists where songs can be:
- added,
- removed,
- displayed in a stable order,
- reordered later.

A plain `ManyToManyField` between playlists and songs would store membership but not the playlist order cleanly.

## Decision

Use a dedicated `PlaylistItem` model linked to:
- `Playlist`
- `Song`

Store order explicitly in the `position` field.

## Consequences

Positive:
- playlist order is first-class data
- reordering is possible without guessing from timestamps
- playlist items can later store more metadata if needed

Trade-offs:
- more code than a plain many-to-many field
- reorder logic must preserve position uniqueness
- serializers and views need to work with an extra model layer

## Notes

This decision matches the project requirements, which explicitly expect strong relationship handling and allow a custom through-style table for ordered playlists.
