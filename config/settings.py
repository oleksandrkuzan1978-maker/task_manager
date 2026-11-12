"""Настройки Django-проекта task_manager.

Загружает переменные окружения из файла .env в корне проекта;
SECRET_KEY и DEBUG читаются через django-environ. Настраивает приложения,
промежуточные обработчики запросов, шаблоны, SQLite, локализацию
и пути к статическим и загружаемым файлам.
"""
from pathlib import Path
import environ
import os

#from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework.filters import SearchFilter, OrderingFilter

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
env.read_env(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',

    'apps.task.apps.TaskConfig',
    'rest_framework_simplejwt.token_blacklist',
]

REST_FRAMEWORK = {'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',
                                              'rest_framework.filters.SearchFilter',
                                              'rest_framework.filters.OrderingFilter',),
              'DEFAULT_PAGINATION_CLASS': 'apps.views.pagination.TaskCursorPagination',
                  'PAGE_SIZE': 2,
              'DEFAULT_AUTHENTICATION_CLASSES': [
                    'rest_framework_simplejwt.authentication.JWTAuthentication'],
              "DEFAULT_PERMISSION_CLASSES": [
                                 "apps.permissions.IsSuperuserOrAuthenticatedReadOnly",],
              # "DEFAULT_PERMISSION_CLASSES": [
              #       "rest_framework.permissions.IsAuthenticated",],
              }

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

http_request_log = {
            'handlers': ['http_request_file'],
            'level': 'DEBUG',
            'propagate': False,
        }
request_file_log = {'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'sql',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5, # хранить до 5 резервных файлов.
            'encoding': 'utf8',}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
'colored': {
        '()': 'colorlog.ColoredFormatter',
    'format': '{log_color} {levelname}: [{asctime}] - {message}',
    'style': '{',
    'datefmt': '%H:%M:%S',

        'log_colors': {
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red,bg_white',
        },
    },

        'sql': {
            'format': '{levelname}: [{asctime}] - {message}',
            'style': '{',
            'datefmt': '%H:%M:%S',
        }
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',

        },
        'db_request_file': {
            **request_file_log,
            'filename': LOGS_DIR / 'db_logs.log',
        },
        'http_request_file': {
            **request_file_log,
            'filename': LOGS_DIR / 'http_logs.log',
        },

    },
    'loggers': {
        # Отвечает за общие сообщения Django: системные события,
        # предупреждения и другие сообщения фреймворка
        # 'django': {
        # 'handlers': ['console'],
        # 'level': 'DEBUG',
        # },

        # Отвечает за сообщения, связанные с обработкой HTTP-запросов и ошибками при их выполнении
        'django.request': http_request_log,
        # Собственный логгер. Отвечает за сообщения, связанные с обработкой HTTP-запросов
        'http': http_request_log,

        # Отвечает за сообщения, связанные с работой шаблонов Django
        'django.template': {
        },

        # Отвечает за SQL-запросы к базе данных
        'django.db.backends': {
            'handlers': ['db_request_file'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Подключение middleware settings.py
    'logs.middleware.RequestLoggingMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}
