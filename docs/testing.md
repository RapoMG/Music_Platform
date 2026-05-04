# Testing

## Current Automated Tests

The repository already includes tests in:
- `backend/apps/catalog/tests/`
- `backend/apps/consumers/tests.py`
- `backend/apps/users/tests.py`

At the moment, the strongest visible coverage is around catalog models and serializers.

## Run Tests

Without Docker:

```bash
cd backend
python manage.py test
```

With Docker:

```bash
docker compose exec web python manage.py test
```

## Recommended Test Priorities

For this project, the highest-value tests are:
- playlist ordering and reorder behavior,
- library deduplication,
- profile and playlist access control,
- published-only album and artist presentation rules,
- serializer output for playlist and library endpoints,
- seed command smoke coverage where practical.

## Testing Philosophy

Prefer a balanced mix of:
- model tests for constraints and ordering,
- service tests for playlist and library logic,
- view/API tests for permissions and response shape.

That will give better protection than relying only on view tests.
