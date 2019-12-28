import os
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "4_s!_h@mqyxiyw2=wg+ol190@4rkx%g!(ch9irmurhzw^gv*f="

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # shop
    "shop.apps.ShopConfig",
    "cart.apps.CartConfig",
    "orders.apps.OrdersConfig",
    "coupons.apps.CouponsConfig",
    # dev
    "django_extensions",
    "debug_toolbar",
    "rosetta",
    "parler",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "myshop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cart.context_processors.cart",
            ]
        },
    }
]

WSGI_APPLICATION = "myshop.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "shopdb.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

PASSWD_VALI_PREFIX = "django.contrib.auth.password_validation."
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{PASSWD_VALI_PREFIX}UserAttributeSimilarityValidator"},
    {"NAME": f"{PASSWD_VALI_PREFIX}MinimumLengthValidator"},
    {"NAME": f"{PASSWD_VALI_PREFIX}CommonPasswordValidator"},
    {"NAME": f"{PASSWD_VALI_PREFIX}NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# See https://github.com/django/django/blob/master/django/conf/global_settings.py
LANGUAGES = (
    ("en-gb", _("English")),
    ("de", _("German")),
    ("zh-hant", _("Traditional Chinese")),
)

# See http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-gb"

# See https://github.com/python/cpython/blob/3.6/Lib/locale.py
# Also
#   When you use the `makemessages` command, the files would be generated in
#   the 'locale/LANG/' we created. For applications with a 'locale/' folder,
#   message files would be generated in THAT directory.
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale/"),)

USE_I18N = True
USE_L10N = True

TIME_ZONE = "UTC"
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# Application-related files (CSS, JavaScript, Images etc.)

# When you go into production phase, this also needs to be changed
STATIC_URL = "/static/"

# Well, for my part, I've put all the (static) files directly into
# the 'PROJECT/static/' (DO NOT DO THAT AGAIN!!!) folder. As for
# (every) other people's method, the files might be put under each apps,
# e.g. for app 'cart',
#   it's 'cart/templates/cart/*' and 'cart/static/cart/*'.
#   The 'cart' before the '*' was meant to "naming" each apps.
# One last thing, for this folder (see https://bit.ly/376I4uA)
# ~ it  is     NOT  for development (STATICFILES_DIRS does)
# ~ it  should be   served by a webserver (e.g. Nginx)
# ~ you should NOT  put anything into it (manually)
# ~ you should only run 'collectstatic' to pour the files into it
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")

# An error being raised
#   "The STATICFILES_DIRS setting should not contain the STATIC_ROOT setting"
# Solution (only a temporary one)
#   The short one     This config shouldn't contain the `STATIC_ROOT` path
#   The long  one     https://stackoverflow.com/a/12161409/6273859
# Other than that, you should know (summed thoughts, maybe not 100% correct)
# - folders list here would be the one '{% static 'FILE' %}' point to
# - :dev , simply use '.. = [os.path.join(BASE_DIR, YOUR_STATIC_FILES/)]'
# - :prod, 'collectstatic', copy all the files to '.._ROOT' (Nginx serves it)
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static/")]

# User-uploaded files (different from the purpose of 'STATIC_XXXX')
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


# Email

EMAIL_BACKEND = os.getenv("CURRENT_EMAIL_BACKEND")


# Session

CART_SESSION_ID = "cart"


# Third-party libraries :: Debugging

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]


# Third-party libraries :: Task queue

# If you're using RabbitMQ, you don't need any initial configurations.
# For Redis, you need a bit of work, see these links for more:
# ~ https://stackabuse.com/asynchronous-tasks-using-flask-redis-and-celery/
# ~ https://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html
# ~ https://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# Execute tasks locally in a synchronous way instead of sending them
# into a queue. Add this if you wanna disable Celery temporarily.
# CELERY_ALWAYS_EAGER = True


# Third-party libraries :: i18n

# fmt: off
PARLER_LANGUAGES = {
    None: (
        {"code": "en-gb"},
        {"code": "de"},
        {"code": "zh-hant"},
    ),
    "default": {
        "fallbacks": ["en-gb"],
        "hide_translated": False,
    },
}
