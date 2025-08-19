import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv
# from urllib.parse import urlparse

load_dotenv()

ADMIN_MAIL = os.getenv('ADMIN_MAIL')
ADMIN_DEFAULT_PASSWORD = os.getenv('ADMIN_DEFAULT_PASSWORD')

ALLOWED_HOSTS = ['*']

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

AUTH_USER_MODEL = 'users.CustomUser'

BASE_DIR = Path(__file__).resolve().parent.parent

CACHE_ENABLED = False


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'{os.getenv("REDIS_HOST")}://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}/1',
    }
}

# URL-адрес брокера сообщений
CELERY_BROKER_URL = f'{os.getenv("CELERY_HOST")}://{os.getenv("CELERY_HOST")}:{os.getenv("CELERY_PORT")}/0'
# Redis, который по умолчанию работает на порту 6379

# URL-адрес брокера результатов, также Redis
CELERY_RESULT_BACKEND = f'{os.getenv("CELERY_HOST")}://{os.getenv("CELERY_HOST")}:{os.getenv("CELERY_PORT")}/0'

# Часовой пояс для работы Celery
CELERY_TIMEZONE = "Europe/Moscow"

# Флаг отслеживания выполнения задач
CELERY_TASK_TRACK_STARTED = True

# Максимальное время на выполнение задачи
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BEAT_SCHEDULE = {
    'task-name': {
        'task': 'tracker.tasks.prepare_dayly_notifications',  # Путь к задаче
        'schedule': timedelta(days=1),  # Расписание выполнения задачи
    },
}

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',  # Замените на адрес вашего фронтенд-сервера
]

CSRF_TRUSTED_ORIGINS = [
    "https://read-and-write.example.com",  # Замените на адрес вашего фронтенд-сервера
    # и добавьте адрес бэкенд-сервера
]

CORS_ALLOW_ALL_ORIGINS = False

CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False


DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# e-mail settings
DEFAULT_FROM_EMAIL = os.getenv('SERVER_MAIL_USER')
EMAIL_HOST = os.getenv('SERVER_MAIL_HOST')
EMAIL_PORT = os.getenv('SERVER_MAIL_PORT')
EMAIL_HOST_USER = os.getenv('SERVER_MAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('SERVER_MAIL_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    'django.contrib.sites',
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework_simplejwt",
    'rest_framework',
    "drf_yasg",
    "corsheaders",
    "django_celery_beat",
    "tracker",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]

# Настройки JWT-токенов
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

ROOT_URLCONF = "config.urls"

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

TELEGRAM_URL = 'https://api.telegram.org/bot'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_THOUSAND_SEPARATOR = True

USE_TZ = True

SECRET_KEY = os.getenv("SECRET_KEY")
SITE_ID = 1
STATIC_URL = "static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
