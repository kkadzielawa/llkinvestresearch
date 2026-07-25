# LLK Investment Research

LLK Investment Research is a Django publishing site for long-form market commentary, sector notes, and investor-facing analysis.

## Technical Stack

- Backend: Django 5.2
- Frontend: HTML, CSS, Vanilla JavaScript
- Database: PostgreSQL
- Deployment: Docker Compose plus GitHub Actions over SSH

## Local Setup

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. For local Docker development, point `DATABASE_URL` at the Compose database host:

```env
DATABASE_URL=postgres://llkinvestresearch:llkinvestresearch@db:5432/llkinvestresearch
```

3. Start the stack:

```bash
docker compose up --build
```

4. Create an admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

If you prefer a non-Docker local setup, install dependencies into a virtualenv, run a local PostgreSQL instance, and then use:

```bash
python manage.py migrate
python manage.py runserver
```

## Development

Run checks and tests:

```bash
docker compose exec web python manage.py check
docker compose exec web python manage.py check --deploy
docker compose exec web python manage.py test
```

Rich text blog content is treated as trusted admin-authored content and is rendered as HTML on article pages.

## Production

Use `docker-compose.prod.yml` on the production host with a populated `.env`:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

For production, set at least:

```env
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com
DATABASE_URL=postgres://llkinvestresearch:replace-db-password@db:5432/llkinvestresearch
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
POSTGRES_DB=llkinvestresearch
POSTGRES_USER=llkinvestresearch
POSTGRES_PASSWORD=replace-db-password
```

## CI/CD

This repo includes a GitHub Actions workflow at `.github/workflows/deploy.yml` that runs on pushes to the `deploy` branch and on manual dispatch.

- `main` is the working branch.
- `deploy` is the production branch.
- Merge `main` into `deploy` to trigger production deployment.

The workflow:

- Runs Django CI checks against PostgreSQL.
- SSHes into the deployment host and runs `scripts/deploy-production.sh`.
- Optionally runs an HTTPS smoke check if `PRODUCTION_URL` is defined as a repository variable or secret.

Required GitHub repository secrets:

```text
DO_HOST
DO_USER
DO_SSH_KEY
DO_SSH_PORT
DO_APP_DIR
```

Optional GitHub repository secret or variable:

```text
PRODUCTION_URL
```
