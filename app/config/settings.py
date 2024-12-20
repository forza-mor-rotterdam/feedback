import locale
import logging
import os
import sys
from os.path import join

import requests
import urllib3

logger = logging.getLogger(__name__)

locale.setlocale(locale.LC_ALL, "nl_NL.UTF-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRUE_VALUES = [True, "True", "true", "1"]

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", os.environ.get("DJANGO_SECRET_KEY"))

GIT_SHA = os.getenv("GIT_SHA")
DEPLOY_DATE = os.getenv("DEPLOY_DATE", "")
ENVIRONMENT = os.getenv("ENVIRONMENT")
DEBUG = ENVIRONMENT == "development"

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

USE_TZ = True
TIME_ZONE = "Europe/Amsterdam"
USE_L10N = True
USE_I18N = True
LANGUAGE_CODE = "nl-NL"
LANGUAGES = [("nl", "Dutch")]

DEFAULT_ALLOWED_HOSTS = ".forzamor.nl,localhost,127.0.0.1"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", DEFAULT_ALLOWED_HOSTS).split(",")

ENABLE_DJANGO_ADMIN_LOGIN = os.getenv("ENABLE_DJANGO_ADMIN_LOGIN", True) in TRUE_VALUES

SIGNALEN_API = os.getenv("SIGNALEN_API")
MELDING_API = os.getenv("MELDING_API")
APPLICATIE_BASIS_URL = os.getenv("APPLICATIE_BASIS_URL")
ALLOW_UNAUTHORIZED_MEDIA_ACCESS = (
    os.getenv("ALLOW_UNAUTHORIZED_MEDIA_ACCESS", False) in TRUE_VALUES
)
TOKEN_API_RELATIVE_URL = os.getenv("TOKEN_API_RELATIVE_URL", "/api-token-auth/")
MELDINGEN_TOKEN_TIMEOUT = 60 * 5

INSTALLED_APPS = (
    "apps.health",
    "django.contrib.humanize",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.gis",
    "django.contrib.postgres",
    "django.forms",
    "webpack_loader",
    "corsheaders",
    "health_check",
    "health_check.cache",
    "health_check.db",
    "health_check.contrib.migrations",
    "debug_toolbar",
    # Apps
    "apps.authenticatie",
    "apps.feedback",
)


MIDDLEWARE = (
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django_session_timeout.middleware.SessionTimeoutMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

# django-permissions-policy settings
PERMISSIONS_POLICY = {
    "accelerometer": [],
    "ambient-light-sensor": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "document-domain": [],
    "encrypted-media": [],
    "fullscreen": [],
    "geolocation": [],
    "gyroscope": [],
    "interest-cohort": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "usb": [],
}

STATICFILES_DIRS = (
    [
        "/app/frontend/public/build/",
    ]
    if DEBUG
    else []
)

FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 Mb limit
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 Mb limit


STATIC_URL = "/static/"
STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), "static"))

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), "media"))


# Database settings
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST_OVERRIDE")
DATABASE_PORT = os.getenv("DATABASE_PORT_OVERRIDE")

DEFAULT_DATABASE = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": DATABASE_NAME,  # noqa:
    "USER": DATABASE_USER,  # noqa
    "PASSWORD": DATABASE_PASSWORD,  # noqa
    "HOST": DATABASE_HOST,  # noqa
    "PORT": DATABASE_PORT,  # noqa
}

DATABASES = {
    "default": DEFAULT_DATABASE,
}
DATABASES.update(
    {
        "alternate": DEFAULT_DATABASE,
    }
    if ENVIRONMENT == "test"
    else {}
)


if ENVIRONMENT in ["test", "development"]:
    DJANGO_TEST_EMAIL = os.getenv("DJANGO_TEST_EMAIL", "test@test.com")
    DJANGO_TEST_PASSWORD = os.getenv("DJANGO_TEST_PASSWORD", "insecure")

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
AUTH_USER_MODEL = "authenticatie.Gebruiker"

SITE_ID = 1
SITE_NAME = os.getenv("SITE_NAME", "MOR Feedback")
SITE_DOMAIN = os.getenv("SITE_DOMAIN", "localhost")

SECRET_HASH_KEY = os.getenv("SECRET_HASH_KEY", "hashkeyforzamorfeedback")

# Django security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = "strict-origin"
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
CORS_ORIGIN_WHITELIST = ()
CORS_ORIGIN_ALLOW_ALL = False
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_NAME = "__Host-sessionid" if not DEBUG else "sessionid"
CSRF_COOKIE_NAME = "__Host-csrftoken" if not DEBUG else "csrftoken"
SESSION_COOKIE_SAMESITE = "Strict" if not DEBUG else "Lax"
CSRF_COOKIE_SAMESITE = "Strict" if not DEBUG else "Lax"

# Settings for Content-Security-Policy header
CSP_DEFAULT_SRC = ("'self'",)
CSP_FRAME_ANCESTORS = ("'self'",)
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "blob:",
    "cdnjs.cloudflare.com",
    "cdn.jsdelivr.net",
)
CSP_IMG_SRC = (
    "'self'",
    "data:",
    "cdn.redoc.ly",
    "cdn.jsdelivr.net",
    "map1c.vis.earthdata.nasa.gov",
    "map1b.vis.earthdata.nasa.gov",
    "map1a.vis.earthdata.nasa.gov",
)
CSP_STYLE_SRC = (
    "'self'",
    "data:",
    "'unsafe-inline'",
    "cdnjs.cloudflare.com",
    "cdn.jsdelivr.net",
    "fonts.googleapis.com",
)
CSP_CONNECT_SRC = ("'self'",)
CSP_FONT_SRC = (
    "'self'",
    "fonts.gstatic.com",
)

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.messages.context_processors.messages",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.static",
                "django.template.context_processors.request",
                "config.context_processors.general_settings",
            ],
        },
    }
]

# Sessions are managed by django-session-timeout-joinup
# Django session settings
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Session settings for django-session-timeout-joinup
SESSION_EXPIRE_MAXIMUM_SECONDS = int(
    os.getenv("SESSION_EXPIRE_MAXIMUM_SECONDS", "28800")
)
SESSION_EXPIRE_SECONDS = int(os.getenv("SESSION_EXPIRE_SECONDS", "3600"))
SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = int(
    os.getenv("SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD", "1800")
)

# Frontend tools for development
# Autoreload socket port
DEV_SOCKET_PORT = os.getenv("DEV_SOCKET_PORT", "9000")
WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "POLL_INTERVAL": 0.1,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
        "LOADER_CLASS": "webpack_loader.loader.WebpackLoader",
        "STATS_FILE": (
            "/static/webpack-stats.json"
            if not DEBUG
            else "/app/frontend/public/build/webpack-stats.json"
        ),
    }
}

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "/app/uwsgi.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
    },
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

OIDC_RP_CLIENT_ID = os.getenv("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = os.getenv("OIDC_RP_CLIENT_SECRET")

OIDC_REALM = os.getenv("OIDC_REALM")
AUTH_BASE_URL = os.getenv("AUTH_BASE_URL")
OPENID_CONFIG_URI = os.getenv(
    "OPENID_CONFIG_URI",
    f"{AUTH_BASE_URL}/realms/{OIDC_REALM}/.well-known/openid-configuration",
)
OPENID_CONFIG = {}
try:
    OPENID_CONFIG = requests.get(
        OPENID_CONFIG_URI,
        headers={
            "user-agent": urllib3.util.SKIP_HEADER,
        },
    ).json()
except Exception as e:
    logger.error(f"OPENID_CONFIG FOUT, url: {OPENID_CONFIG_URI}, error: {e}")
OIDC_ENABLED = False
if OPENID_CONFIG and OIDC_RP_CLIENT_ID:
    OIDC_ENABLED = True
    OIDC_VERIFY_SSL = os.getenv("OIDC_VERIFY_SSL", True) in TRUE_VALUES
    OIDC_USE_NONCE = os.getenv("OIDC_USE_NONCE", True) in TRUE_VALUES

    OIDC_OP_AUTHORIZATION_ENDPOINT = os.getenv(
        "OIDC_OP_AUTHORIZATION_ENDPOINT", OPENID_CONFIG.get("authorization_endpoint")
    )
    OIDC_OP_TOKEN_ENDPOINT = os.getenv(
        "OIDC_OP_TOKEN_ENDPOINT", OPENID_CONFIG.get("token_endpoint")
    )
    OIDC_OP_USER_ENDPOINT = os.getenv(
        "OIDC_OP_USER_ENDPOINT", OPENID_CONFIG.get("userinfo_endpoint")
    )
    OIDC_OP_JWKS_ENDPOINT = os.getenv(
        "OIDC_OP_JWKS_ENDPOINT", OPENID_CONFIG.get("jwks_uri")
    )
    OIDC_RP_SCOPES = os.getenv(
        "OIDC_RP_SCOPES",
        " ".join(OPENID_CONFIG.get("scopes_supported", ["openid", "email", "profile"])),
    )
    OIDC_OP_LOGOUT_ENDPOINT = os.getenv(
        "OIDC_OP_LOGOUT_ENDPOINT",
        OPENID_CONFIG.get("end_session_endpoint"),
    )

    if OIDC_OP_JWKS_ENDPOINT:
        OIDC_RP_SIGN_ALGO = "RS256"

    AUTHENTICATION_BACKENDS = [
        "django.contrib.auth.backends.ModelBackend",
        "apps.authenticatie.auth.OIDCAuthenticationBackend",
    ]

    ALLOW_LOGOUT_GET_METHOD = True
    OIDC_STORE_ID_TOKEN = True
    OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = int(
        os.getenv("OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS", "300")
    )

    LOGIN_REDIRECT_URL = "/"
    LOGIN_REDIRECT_URL_FAILURE = "/"
    LOGOUT_REDIRECT_URL = OIDC_OP_LOGOUT_ENDPOINT
    LOGIN_URL = "/oidc/authenticate/"
