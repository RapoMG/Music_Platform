# Setup

## Requirements

- Python environment matching the project dependencies
- PostgreSQL
- Docker and Docker Compose for containerized development
- a `.env.dev` file in the project root

## Running With Docker

From the project root:

```bash
docker compose --env-file .env.dev up --build
```

The main services are:
- `web` - Django application
- `postgres` - PostgreSQL database

Useful commands:

```bash
docker compose up -d
docker compose down
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py test
```

## Running Without Docker

All Django commands should be executed from `backend/` because `manage.py` lives there.

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Static and Media Notes

- templates live under `frontend/templates/`
- static files live under `frontend/static/`
- media files are stored under `backend/media/`

## Environment Notes

The default development settings load environment variables from:

```text
.env.dev
```

Key settings to keep in mind:
- custom user model: `users.User`
- default database: PostgreSQL
- time zone: `Europe/Warsaw`
- language code: `pl-pl`
