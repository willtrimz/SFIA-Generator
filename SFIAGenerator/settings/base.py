"""
Django settings for SFIAGenerator project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
from django.contrib import messages
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY','$9.I0beLhR(V$m=InEgZwF7HD8u^vO8TA(mfW-7U35SLbFSN')

# Application definition

INSTALLED_APPS = [
    'ckeditor',
    'django.contrib.auth',
    'Generator.apps.GeneratorConfig',
    'django.contrib.admin',
    'dynamic_preferences',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
	'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'SFIAGenerator.AdminMiddleware.AdminLocaleURLMiddleware',
]

ROOT_URLCONF = 'SFIAGenerator.urls'

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
                'django.template.context_processors.request',
                'dynamic_preferences.processors.global_preferences',
            ],
        },
    },
]

WSGI_APPLICATION = 'SFIAGenerator.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

ADMIN_LANGUAGE_CODE='en'

# Path for the translation files
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

# Available languages
LANGUAGES = [
	('en', 'English'),
	('cy', 'Cymraeg'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Stops the text being automatically encased in <p> tags when editing/creating an individual SFIA skill
# Also removes toolbar formatting options toolbar from form, leaving only undo and redo button
CKEDITOR_CONFIGS = {
    'default': {
        'autoParagraph': False,
        'toolbar': [{'items':['Undo', 'Redo']}]
    },
}

DYNAMIC_PREFERENCES = {

    # a python attribute that will be added to model instances with preferences
    # override this if the default collide with one of your models attributes/fields
    'MANAGER_ATTRIBUTE': 'preferences',

    # The python module in which registered preferences will be searched within each app
    'REGISTRY_MODULE': 'dynamic_preferences_registry',

    # Allow quick editing of preferences directly in admin list view
    # WARNING: enabling this feature can cause data corruption if multiple users
    # use the same list view at the same time, see https://code.djangoproject.com/ticket/11313
    'ADMIN_ENABLE_CHANGELIST_FORM': False,

    # Customize how you can access preferences from managers. The default is to
    # separate sections and keys with two underscores. This is probably not a settings you'll
    # want to change, but it's here just in case
    'SECTION_KEY_SEPARATOR': '__',

    # Use this to disable caching of preference. This can be useful to debug things
    'ENABLE_CACHE': True,

    # Use this to disable checking preferences names. This can be useful to debug things
    'VALIDATE_NAMES': True,
}

# Changes the 'error' message tag to 'danger' so it can be recognised for styling by bootstrap
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}