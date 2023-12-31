#-*- coding: utf-8 -*-
# django-debug-toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]
"""
Django settings for site_honey project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from django.contrib.messages import constants as messages
#import mimetypes
#mimetypes.add_type("text/css", ".css", True)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = "django-insecure-m%)&d$8ov$acr8@(n2lb&17otx2*i1_ba_9j6g%fg05m$mnl^&"
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# `ALLOWED_HOSTS = ['***.ru','www.***.ru', u'156.168.']`

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.sites',
    'debug_toolbar',
    # 'channels',
    'django.contrib.humanize',

    # стандартные пакеты
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',

    'crispy_forms',
    'ckeditor',

    # Мои приложения
    # когда применяем сигналы, метки лучше указать полный путь
    # В общем случае можно использовать просто название приложения

    'catalog.apps.CatalogConfig',
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'notification',

    # должна быть последней
    'django_cleanup.apps.CleanupConfig',
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware', # django-debug-toolbar
]

ROOT_URLCONF = "site_honey.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates'),
                 ],
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

# django-allauth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIAL_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    }
}

# END django-allauth


WSGI_APPLICATION = "site_honey.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db_honey_site_2.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# (https://docs.djangoproject.com/en/4.2/ref/settings/#static-root)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
"""
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "other_static"),
]
"""

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#CRISPY_TEMPLATE_PACK = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'uni_form'

#https://docs.djangoproject.com/en/4.2/ref/settings/#login-url
LOGIN_REDIRECT_URL = 'blog-home'#blog/views.py первая ссылка на index.html
LOGIN_URL = 'account_login'

CKEDITOR_CONFIGS = {
    'default': {
        'width':'auto',
    },
}

#django-channels
ASGI_APPLICATION = "honeymelon_handmade_jewerly.routing.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}
# End django-channels

# Email
#для боевого сервера
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Email
# для отладки
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Email
# для отладки
EMAIL_HOST = 'smpt.gmail.com'
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_HOST_USER =os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASS')
# End email

GOOGLE_RECAPTCHA_SECRET_KEY = os.getenv("GOOGLE_RECAPTCHA_SECRET_KEY")

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-succesS',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


#В ПРОИЗВОДСТВЕ УБРАТЬ!
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"