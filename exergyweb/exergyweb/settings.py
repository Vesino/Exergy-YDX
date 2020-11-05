"""
Django settings for exergy_webpage project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = '/static/'
#STATICFILES_DIRS = [
 #  os.path.join(BASE_DIR, "static"),
  # ]
   
STATIC_ROOT = 'static'

#PROYECT_ROOT = os.path.abspath(os.path.dirname(__file__))

#STATICFILES_DIRS = (
 #   os.path.join(PROYECT_ROOT, 'static'),
#)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dok)dh=1-0%%p2gu$l8l&(6w!k!3e&u*wxsp7mpz9m+k896(=@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    'exergyapp',
    'crispy_forms',
]

MIDDLEWARE = [
    #'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'exergyweb.urls'

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

WSGI_APPLICATION = 'exergyweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

#ALLOWED_HOSTS = ['exergywebpage.herokuapp.com'
'''ALLOWED_HOSTS = ['django-env.kyq396crum.eu-central-1.elasticbeanstalk.com', 'dualstack.awseb-e-m-AWSEBLoa-1UL9K6YOPAOG-852094795.eu-central-1.elb.amazonaws.com', 'django-env.zeffhmrdge.us-west-2.elasticbeanstalk.com', 'dualstack.awseb-e-v-AWSEBLoa-L7TJQJBZWDXI-1150898848.us-west-2.elb.amazonaws.com', 'http://www.exergy-tech.com/', 'www.exergy-tech.com', 'exergy-tech.com', 'http://exergy-tech.com']
'''
ALLOWED_HOSTS = ['django-env.kyq396crum.eu-central-1.elasticbeanstalk.com', 'dualstack.awseb-e-m-AWSEBLoa-1UL9K6YOPAOG-852094795.eu-central-1.elb.amazonaws.com', 'django-env.zeffhmrdge.us-west-2.elasticbeanstalk.com', 'dualstack.awseb-e-v-AWSEBLoa-L7TJQJBZWDXI-1150898848.us-west-2.elb.amazonaws.com', 'http://www.exergytech.co/', 'www.exergytech.co', 'exergytech.co', 'http://exergytech.co', '127.0.0.1', 'localhost']

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/



#  Add configuration for static files storage using whitenoise
#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
