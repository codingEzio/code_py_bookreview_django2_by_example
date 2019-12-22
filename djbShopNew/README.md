### Getting Started
- Install packages
  ```bash
  pipenv install                # dev
  pipenv install --dev --pre    # linter, formatter
  ```

- Initialize project & apps
  ```bash
  $ django-admin startproject myshop && cd myshop
  $ django-admin startapp     cart
  ```

- Create needed folders
  ```bash
  $ mkdir templates/    # HTML templates
  $ mkdir static/       # Application-related files (.js,  .css etc.)
  $ mkdir media/        # User-uploaded       files (.jpg, .png etc.)
  ```

- Configure *templates* <small>(settings.py)</small>
  ```python
  TEMPLATES = [
    {
      .. ,
      "DIRS": [os.path.join(BASE_DIR, "templates/")],
      .. ,
    }
  ]
  ```

- Configure new *app* <u>cart</u> <small>(multiple files)</small>
  ```python
  # settings.py
  INSTALLED_APPS = [
    "shop.apps.ShopConfig",
  ]

  # urls.py    (PROJ/cart/urls.py) (create it if you don't have one)
  from django.urls import path
  from .           import views
  app_name = "shop"

  # urls.py    (project-level)
  from django.urls import include
  urlpatterns = [
    # add to the bottom of 'urlpatterns' (MUST)
    path("", include("shop.urls", namespace="shop",)),
  ]
  ```

- Configure [*static files*](https://docs.djangoproject.com/en/3.0/howto/static-files/) <small>(multiple files)</small>
  ```python
  # settings.py
  STATIC_URL = "/static/"
  STATICFILESS_DIRS = [os.path.join(BASE_DIR, "static/")]
  MEDIA_URL = "/media/"
  MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

  # urls.py    (project-level)
  from django.conf import settings
  from django.conf.urls.static import static

  if settings.DEBUG:
    urlpatterns += static(
      prefix=settings.MEDIA_URL,
      document_root=settings.MEDIA_ROOT,
    )
  ```

- Configure `.env` <small>(multiple files)</small>
  ```python
  # manage.py
  from pathlib import Path
  from dotenv import load_dotenv

  def main():
    env_path = Path("..") / ".env"
    load_dotenv(dotenv_path=env_path)

  # Usage: settings.py
  EMAIL_BACKEND = os.getenv("CURRENT_EMAIL_BACKEND")  # an example
  ```

- Configure [django-extensions](https://pypi.org/project/django-extensions/) <small>(settings.py)</small>
  ```python
  INSTALLED_APPS = [
    # add to the bottom of 'INSTALLED_APPS'
    "django_extensions",
  ]
  ```

- Configure [*django-debug-toolbar*](https://pypi.org/project/django-debug-toolbar/) <small>(multiple files)</small>
  ```python
  # settings.py

  INSTALLED_APPS = [
    # add to the bottom of 'INSTALLED_APPS'
    "debug_toolbar",
  ]
  MIDDLEWARE = [
    # add to the bottom of 'MIDDLEWARE'
    "debug_toolbar.middleware.DebugToolbarMiddleware",  
  ]
  DEBUG_TOOLBAR_PANELS = [
    # comment out what you don't actually need
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


  # urls.py    (project-level)

  if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
      path("__debug__/", include(debug_toolbar.urls))
    ]
  ```
