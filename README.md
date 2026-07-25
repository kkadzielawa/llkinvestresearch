# LLK Investment Research

LLK Investment Research is a Django publishing site for market commentary, long-form research notes, and contact inquiries.

## Local Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file:

```bash
cp .env.example .env
```

Run migrations and create an admin user:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Run the test suite:

```bash
python manage.py test
```

## Environment Variables

The project reads configuration from environment variables.

- `SECRET_KEY`: Django secret key.
- `DEBUG`: `True` for local development, `False` for production.
- `ALLOWED_HOSTS`: Comma-separated hostnames.
- `DATABASE_NAME`: SQLite database filename or absolute path.
- `DEFAULT_FROM_EMAIL`: Outgoing sender address for contact form emails.
- `CONTACT_EMAIL`: Inbox for contact form submissions.
- `EMAIL_BACKEND`: Django email backend path.

Rich text blog content is treated as trusted admin-authored content and is rendered as HTML on article pages.

## Deployment Notes

Static files are served from `static/` in development and collected into `staticfiles/` for deployment:

```bash
python manage.py collectstatic --noinput
```

Gunicorn entry point:

```bash
gunicorn llkinvestresearch.wsgi
```
