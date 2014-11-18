"""
Django settings for webapp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Used for third-party login
FACEBOOK_APP_ID              = '1482123585385436'
FACEBOOK_API_SECRET          = '01a4982a4d38517e15d93eaffcf53db3'

TWITTER_CONSUMER_KEY = 'DeJb7nP7haOPwf8l8ZyunXZlK'
TWITTER_CONSUMER_SECRET = '7cjXRjw2WAAsN5pbzDYBfTjkBJVc8arydniwq0MA2EF2x8cvmg'

SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v*nq@da9$zu%i6&icv3ku=+zm$9ox_!&9(h340zmi-n&btr1py'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'selectable',
    'foodchaser',
    'social_auth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.twitter.TwitterBackend',
    'django.contrib.auth.backends.ModelBackend'
 )

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Enable real email sending
# Need to comment out 
EMAIL_HOST = "smtp.andrew.cmu.edu"
EMAIL_HOST_USER = "huiwenz@andrew.cmu.edu"
EMAIL_HOST_PASSWORD = "" 
EMAIL_USE_TLS = True


ROOT_URLCONF = 'webapp.urls'

# Used by the authentication system for the application.
# URL to use if the authentication system requires a user to log in.
# our log-in page
LOGIN_URL = '/'

# Default URL to redirect to after a user logs in. Set it to foodchaser.
LOGIN_REDIRECT_URL = '/foodchaser/userhome'

WSGI_APPLICATION = 'webapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
