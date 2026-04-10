Commands
# Commands

All commands below are executed from the project root.

## With Docker

### Build add start environment
Compose only uses a .env file (no extension) next to docker-compose.yml for interpolation. .env.dev must be named explicitly.

```bash
docker compose --env-file .env.dev up --build
```

### Start local environment

```bash
docker compose up -d
```

### Stop local environment

```bash
docker compose down
```

### Execute command in Terminal while Docker containeris working
These are the versions of commands run from the IDE terminal or PowerShell

```bash
docker compose exec <service name> python manage.py <command>
```
Example:

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py test
```

## Inside Docker container shell

### Run Django management commands
```bash
python backend/manage.py <command>
```
Example:

```bash
python backend/manage.py migrate
python backend/manage.py createsuperuser
python backend/manage.py runserver
```

### Create migrations
```bash
python backend/manage.py makemigrations
```

### Apply migrations
```bash
python backend/manage.py migrate
```

### Create superuser
```bash
python backend/manage.py createsuperuser
```

### Collect static files
```bash
python backend/manage.py collectstatic --noinput
```

### Run tests
```bash
python backend/manage.py test
```

### Create a new Django app
```bash
python backend/manage.py startapp app_name backend/apps/app_name
```
After creating the app, move configuration files if needed and register the app in settings.

### Open Django shell
```bash
python backend/manage.py shell
```

### Run development server without Docker
```bash
python backend/manage.py runserver
```

