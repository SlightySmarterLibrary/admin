"""
Django settings for webapp project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from envs import env
import boto3

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '***REMOVED***'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = [
    'djwarrant.backend.CognitoBackend',
    'django.contrib.auth.backends.ModelBackend'
]

DYNAMODB_BOOKS = 'SSL-Books'

COGNITO_ATTR_MAPPING = env(
    'COGNITO_ATTR_MAPPING',
    {
        'username': 'username',
        'email': 'email',
        'name': 'name',
        'custom:api_key': 'api_key',
        'custom:api_key_id': 'api_key_id'
    },
    var_type='dict')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library',
    'djwarrant',
    'crispy_forms',
    'django_extensions',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'library/templates'),
        ],
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

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

WSGI_APPLICATION = 'webapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

LOGIN_REDIRECT_URL = '/accounts/profile'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CRISPY_TEMPLATE_PACK = 'bootstrap3'

***REMOVED*** = 'ASIAT6STUTTCM5T5AGLD'
***REMOVED*** = 'zMtMRmhqMZGzJ3GRqhbsMQL1XTQsllcCpJBwDkns'
AWS_REGION = 'us-east-1'
COGNITO_NAME = 'maskidentity'

# ================================================================
# This section automatically loads user cognito information for user pool
# and identity pools on AWS. The entry point for this is the `COGNITO_NAME`
# defined above that is the name for the congito pool, cognito client, and identify pool.

cognito = boto3.client('cognito-idp', region_name=AWS_REGION)

# Load the UserPool ID for the smart library.
for user_pool in cognito.list_user_pools(MaxResults=5)['UserPools']:
    if user_pool['Name'] == COGNITO_NAME:
        user_pool_id = user_pool['Id']
        break

# Load UserPool Clients.
for client in cognito.list_user_pool_clients(UserPoolId=user_pool_id, MaxResults=10)['UserPoolClients']:
    if client['ClientName'] == COGNITO_NAME:
        user_client_id = client['ClientId']

# Load IdentifyPoolId for the Smart Library
cognito_identity = boto3.client(
    'cognito-identity', region_name=AWS_REGION)

for pool in cognito_identity.list_identity_pools(MaxResults=10)['IdentityPools']:
    if pool['IdentityPoolName'] == COGNITO_NAME:
        identity_pool_id = pool['IdentityPoolId']
        break

COGNITO_IDENTITY_POOL = identity_pool_id
COGNITO_USER_POOL_ID = user_pool_id
COGNITO_APP_ID = user_client_id

# ================================================================

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
