import os

NOTES = """
Setup postgreSQL database at the very outset
    Basic steps
    [1] System
        $ brew   install postgresql && brew services restart postgresql
        $ pipenv install psycopg2-binary==2.7.4
    [2] PostgreSQL
        $ createuser -dP PSQL_USER_NAME
        $ createdb -E utf-8 -U PSQL_USER_NAME PSQL_DATABASE_NAME
        ~ run `dropdb DATABASE_NAME` to delete unwanted databases
        ~ if you can't, check who's using it: https://stackoverflow.com/a/7073852/6273859
    [3] Django
        >> 'ENGINE'  : 'django.db.backends.postgresql',
        >> 'NAME'    : os.environ.get('POSTGRESQL_DB_NAME_BKMK'),
        >> 'USER'    : os.environ.get('POSTGRESQL_USER'),
        >> 'PASSWORD': os.environ.get('POSTGRESQL_PASSWORD'),
    [4] Final
        $ ./manage.py migrate
        
Other stuff needs to be done before we started
    Install 'python-dotenv'
    1) pipenv install python-dotenv
    2) configure at 'ROOT/manage.py' (mainly trying to find the '.env' file)
    3) write that '.env' file (for me, it lives at the root level of my repo)
    
    Create superusers
    $ ./manage.py createsuperuser
    

"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%z%fhnp6o30=re7u=^s+ks1a832^uw7fkx14zm=ma*mx_(oh-&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    # default
    'localhost',
    '127.0.0.1',
    '[::1]',
]


# Application definition

INSTALLED_APPS = [
    'account.apps.AccountConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


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

ROOT_URLCONF = 'djbBookmark.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'djbBookmark.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.postgresql',
        'NAME'    : os.environ.get('POSTGRESQL_DB_NAME_BKMK'),
        'USER'    : os.environ.get('POSTGRESQL_USER'),
        'PASSWORD': os.environ.get('POSTGRESQL_PASSWORD'),
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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

