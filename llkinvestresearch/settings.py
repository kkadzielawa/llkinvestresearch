import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def get_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_list(name, default):
    value = os.getenv(name)
    if not value:
        return default
    return [item.strip() for item in value.split(",") if item.strip()]


def get_int(name, default=0):
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "llkinvestresearch-local-dev-secret-key-2026-verify-before-production-8a7f3c2d9e",
)
DEBUG = get_bool("DEBUG", default=True)
ALLOWED_HOSTS = get_list(
    "ALLOWED_HOSTS",
    ["127.0.0.1", "localhost", "llkinvestresearch.herokuapp.com"],
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog.apps.BlogConfig",
    "ckeditor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "llkinvestresearch.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "llkinvestresearch.wsgi.application"

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    postgres_db = os.getenv("POSTGRES_DB", "llkinvestresearch")
    postgres_user = os.getenv("POSTGRES_USER", "llkinvestresearch")
    postgres_password = os.getenv("POSTGRES_PASSWORD", "llkinvestresearch")
    postgres_host = os.getenv("POSTGRES_HOST", "127.0.0.1")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")
    DATABASE_URL = (
        f"postgres://{postgres_user}:{postgres_password}"
        f"@{postgres_host}:{postgres_port}/{postgres_db}"
    )

DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
if DEBUG:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

CSRF_TRUSTED_ORIGINS = get_list("CSRF_TRUSTED_ORIGINS", [])
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "research@llkinvest.local")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", DEFAULT_FROM_EMAIL)
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)

SESSION_COOKIE_SECURE = get_bool("SESSION_COOKIE_SECURE", default=not DEBUG)
CSRF_COOKIE_SECURE = get_bool("CSRF_COOKIE_SECURE", default=not DEBUG)
SECURE_SSL_REDIRECT = get_bool("SECURE_SSL_REDIRECT", default=not DEBUG)
SECURE_REFERRER_POLICY = os.getenv("SECURE_REFERRER_POLICY", "same-origin")
SECURE_HSTS_SECONDS = get_int(
    "SECURE_HSTS_SECONDS",
    default=31536000 if not DEBUG else 0,
)
SECURE_HSTS_INCLUDE_SUBDOMAINS = get_bool(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=not DEBUG,
)
SECURE_HSTS_PRELOAD = get_bool("SECURE_HSTS_PRELOAD", default=not DEBUG)
