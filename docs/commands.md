# Commands

All examples below assume the current repository layout, where `manage.py` is located in `backend/`.

## Docker

### Build and start

```bash
docker compose --env-file .env.dev up --build
```

### Start in background

```bash
docker compose up -d
```

### Stop services

```bash
docker compose down
```

### Run Django commands inside the web container

```bash
docker compose exec web python manage.py <command>
```

Examples:

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py test
```

## Local Development

Change into `backend/` first:

```bash
cd backend
```

Then run commands such as:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py test
python manage.py shell
```

## Migrations

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

## Static Files

```bash
cd backend
python manage.py collectstatic --noinput
```

## Create a New App

```bash
cd backend
python manage.py startapp app_name apps/app_name
```

After creating an app:
- move files if needed,
- register the app in settings,
- wire URLs if the app exposes views.

## Seed Catalog Data

```bash
cd backend
python manage.py seed_catalog
```

Arguments:
- `--artists` default `5`
- `--albums` default `3`
- `--songs` default `10`
- `--genres` default `6`

Example:

```bash
cd backend
python manage.py seed_catalog --artists 7 --songs 12
```

Docker equivalent:

```bash
docker compose exec web python manage.py seed_catalog --artists 7 --songs 12
```
