"""
Django settings for IMMS project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from decouple import config
import dj_database_url
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-broma9&a4p=45&39qr_+_uj2febocbyi(+x)y+58!umgwh-5q_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",
    'mess',
    'payments',
    'drf_social_oauth2',
    "rest_framework",
    "rest_framework.authtoken",
    'oauth2_provider',
    'social_django',
    'corsheaders',
    'allauth',
    # 'background_task',
    # "django_cron",
    'django_crontab',
]
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
# Disable email verification since this is just a test.
# If you want to enable it, you'll need to configure django-allauth's email confirmation pages

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
# SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
# SOCIALACCOUNT_EMAIL_REQUIRED = False
# SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
#         'hd': 'iiitdmj.ac.in'
#     }

# SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['iiitdmj.ac.in']
# REST_USE_JWT = True

SITE_ID = 1

from datetime import timedelta

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
#     'ROTATE_REFRESH_TOKENS': True, # IMPORTANT
#     'BLACKLIST_AFTER_ROTATION': True, # IMPORTANT
#     'UPDATE_LAST_LOGIN': True,
# }


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True
# Rest Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
    # 'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
]
}
AUTHENTICATION_BACKENDS = (
   'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'IMMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'IMMS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'imms',
#         'USER': 'messuser',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# DATABASE={
#     "deafult":dj_database_url.parse(os.environ.get("DATABASE_URL"))
# }

DATABASES = {
    'default': dj_database_url.config(
        # Feel free to alter this value to suit your needs.
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600
    )
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# AUTH_USER_MODEL = 'mess.User' 
CORS_ALLOWED_ORIGINS = ["http://localhost:3000",    ]

# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
#     'https://www.googleapis.com/auth/userinfo.email',
#     'https://www.googleapis.com/auth/userinfo.profile',
# ]

CRONJOBS = [
    ('30 11 * * *', 'mess.cron.my_cron_job'),
    ('30 3 * * *', 'mess.cron.my_cron_job'),
    ('30 23 * * *', 'mess.cron.my_cron_job'),
    ('30 0 * * *', 'mess.cron.get_registered_user'),
]

SITE_URL='http://localhost:3000'

STRIPE_SECRET_KEY=os.environ.get("STRIPE_SECRET_KEY")

# STRIPE_SECRET_KEY='sk_test_51MyXY2SGJ3YbEH6gvCFHMOPNuTH7Cy7cRV3bePnFguEASdeDo2mKtOTvQGLvbKMNgVmZgorw7X0OMUNmbi8AI4Wi00YcdJgeyX'

