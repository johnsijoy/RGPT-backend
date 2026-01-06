"""
Django settings for realestate project.
"""

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# GIS LIBRARIES
# =========================
if os.getenv("RENDER") == "True":
    # Render (Linux) – PostGIS already available
    pass
else:
    # Windows local development
    GDAL_LIBRARY_PATH = r"C:\Users\HP\AppData\Local\Programs\OSGeo4W\bin\gdal311.dll"
    GEOS_LIBRARY_PATH = r"C:\Users\HP\AppData\Local\Programs\OSGeo4W\bin\geos_c.dll"
    os.environ["PROJ_LIB"] = r"C:\Users\HP\AppData\Local\Programs\OSGeo4W\share\proj"

# =========================
# SECURITY
# =========================
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1"
).split(",")

# =========================
# INSTALLED APPS
# =========================
INSTALLED_APPS = [
    "corsheaders",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",

    # Third-party
    "rest_framework",
    "rest_framework_gis",
    "django_filters",

    # Local apps
    "inventory.apps.InventoryConfig",
]

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "realestate.urls"

WSGI_APPLICATION = "realestate.wsgi.application"

# =========================
# DATABASE (Render PostgreSQL / PostGIS)
# =========================
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# =========================
# PASSWORD VALIDATION
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================
# INTERNATIONALIZATION
# =========================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# =========================
# STATIC & MEDIA
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================
# REST FRAMEWORK
# =========================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

# =========================
# JWT
# =========================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=int(os.getenv("JWT_ACCESS_MINUTES", 60))
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=int(os.getenv("JWT_REFRESH_DAYS", 7))
    ),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# =========================
# CORS & CSRF (VERY IMPORTANT)
# =========================
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "https://rgpt-frontend-ym2m.vercel.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://rgpt-frontend-ym2m.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True
