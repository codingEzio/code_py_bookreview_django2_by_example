### Tips
- Wanna try something without actually *running* it?
  ```./manage.py THE_COMMAND --dry-run```
- About *static files*, or `./manage.py collectstatic`
  - Basically, what it does is simply "*copying files from XXX to* `STATIC_ROOT`"
  - The *XXX* might be these places:
    1. Django's built-in static files, like *template*, *CSS* etc. <small>(extending admin? this is the one)</small>
    2. Static files under each apps. One way of organizing things, i.e. `app/{templates|static}/app/FILES`</small>
  - Oh, "*one*" more thing
    - Files that already *in* the folder <small>(i.e. `STATIC_ROOT`)</small> *will* **NOT** be touched.
    - Folders under `STATICFILES_DIRS` will also be copied to the `STATIC_ROOT` directory.
    - The command `collectstatic` *can* be runned at *any* time <small>(before starting the server)</small>, since it's just *static files*.
    - Normally <small>(**during development**)</small>, you *DON'T NEED TO TOUCH THIS* <small>(`collectstatic`)</small>.
- Static files during *dev* & *prod*
  - Note
    - There're already lots of notes inside the `settings.py`, please *go check it out*.
    - Some posts helped me directly, some of them are more like *oh.. that's where things gone wrong..*.
  
  - Here are some *extremly useful* posts
    1. [Github search `STATICFILES_DIRS settings.py` <small>(posts & config, **amazing**!)</small>](https://github.com/search?q=STATICFILES_DIRS+settings.py&type=Code)
    2. [Django設置模闆中 CSS JS 路徑的方法.md](https://github.com/doraemonext/BlogPost/blob/fa7c59535ffffdbd11e8ede04f95d75bd2696e9a/534-Django%E8%AE%BE%E7%BD%AE%E6%A8%A1%E6%9D%BF%E4%B8%AD%20CSS%20JS%20%E8%B7%AF%E5%BE%84%E7%9A%84%E6%96%B9%E6%B3%95.md)  <small>(havn't *read* yet)</small>
    3. [Django 的 STATIC_ROOT 與 STATICFILES_DIRS 的區别.md](https://github.com/xiaomabenten/blog/blob/5eef7892a20edfe7a6a220067c7063e6a377e7bd/content/post/django%E7%9A%84STATIC_ROOT%E4%B8%8ESTATICFILES_DIRS%E7%9A%84%E5%8C%BA%E5%88%AB.md) <small>(*read*, *extremely helpful*)</small>
    4. [st Handling static files that dont pertain to an app in Django](https://stackoverflow.com/questions/22976596/handling-static-files-that-dont-pertain-to-an-app-in-django)
    5. [st serving static files on Django production tutorial](https://stackoverflow.com/a/29087858/6273859)
    6. [Django Static Files](https://rahmonov.me/posts/django-static-files/) <small>(*read*, *extremely helpful*)</small>
- About settings related to *i18n* and *i10n* <small>(*underscore* or *dash* MATTERS)</small>
  - *`LANGUAGES`*
    ```bash
    # Follow https://github.com/django/django/blob/master/django/conf/global_settings.py
    # Examples:
    #   ('de'     , 'German'             )    origin (no variations in settings)
    #   ('es'     , 'Spanish'            )    origin (with variations, not much, mostly in Spanish & English)
    #   ('es-ar'  , 'Argentinian Spanish')    variations
    #   ('zh-hant', 'Traditional Chinese')    variations, but not the same as western languages
    LANGUAGES = (
      ("en-gb", "English"),
      ("de", "German"),
      ("zh-hant", "Traditional Chinese"),
    )
    ```
  - *`LANGUAGE_CODE`*
    ```bash
    # Follow http://www.i18nguy.com/unicode/language-identifiers.html
    #   1. Way more variations than other settings
    #   2. Use lowercase version instead (zh-hant instead of zh-Hant)
    #   3. Choose the "country-related" one from the list (zh-TW, not zh-Hant)
    # Examples:
    #   de-DE
    #   en-GB  , en-US        
    #   zh-Hant, zh-TW        use the latter to achieve greater clarity
    LANGUAGE_CODE = "en-gb"
    ```
  - *`LOCALE_PATHS`* <small>(search `locale_alias` in the link)</small>
    ```bash
    # Follow https://github.com/python/cpython/blob/3.6/Lib/locale.py 
    #   1. This setting itself is nothing special
    #   2. The things you need to care about is the sub-directories 🤓
    # Examples:
    #   zh          China with encoding 'eucCN'                 # don't (too vague) 
    #   zh_cn       China with encoding 'gb2312'                # yes     
    #   zh_cn.euc   China with encoding 'eucCN' (with locale)   # don't (let user care about the encoding)

    # In practice
    #   underscore, lowercase, with-locale
    locale/
      zh_tw/
      de_de/
      en_gb/
    ```
  - Three of them **combined**
    ```bash
    # Examples
    #   ("de", "German")                      de-de     de_de/
    #   ("zh-hant", "Traditional Chinese")    zh-tw     zh_tw/
    ```
- Three stages of *i18n*
  1. *Mark* the stuff you wanna internatonalize <small>(e.g. `_()`, `{% trans %}`)</small>
  2. *Write* the translation <small>(`.po`)</small>
  3. *Compile* the translation files <small>(`.mo`)</small>
- Where to get *translations* <small>(only for *personal* project)</small>
  - What I think is better
    - Websites that offers different languages
    - The references on the [*Linguee*](https://www.linguee.com) website
  - Online translation <small>(best to not-that-good)</small>
    - [Reverso](https://context.reverso.net/translation/)
    - [Linguee](https://www.linguee.com)
    - [Google Translate](https://translate.google.com)
  - Choosing the right word
    - [HiNative](https://hinative.com/)
- Issues you might encounter when using `{% blocktrans %}`
  ```html
  <!-- Do this -->
  {% blocktrans with K=V K=V %} ...
  {% endblocktrans %}

  <!-- Not this -->
  <!-- sometimes the expressions might be really long, well, get with it -->
  {% blocktrans with K=V
                     K=V %} ...
  {% endblocktrans %}

  <!-- Also, don't forget to import the tag -->
  {% load i18n %}
  ```

### Getting Started
- Install packages
  ```bash
  pipenv install                # dev
  pipenv install --dev --pre    # linter, formatter
  ```

- Initialize project & apps
  ```bash
  $ django-admin startproject myshop && cd myshop
  $ django-admin startapp     shop
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

- Configure new *app* <u>shop</u> <small>(multiple files)</small>
  ```python
  # settings.py
  INSTALLED_APPS = [
    "shop.apps.ShopConfig",
  ]

  # urls.py    (PROJ/shop/urls.py) (create it if you don't have one)
  from django.urls import path
  from .           import views
  app_name = "shop"

  # urls.py    (project-level)
  from django.urls import include
  urlpatterns = [
    # comment this out if havn't got any patterns in 'shop/urls.py'
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
