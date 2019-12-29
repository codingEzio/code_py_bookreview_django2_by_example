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
- What is *django-rosetta*
  - A tool that saves you from repetitive commands `compilemessages`
    > Do note that you still need to run `makemessages --all` to gen the translation files <small>(i.e. `.po`)</small>! 
  - Other small things you might wanna know
    1. *Fuzzy* in the django-rosetta page means <q>this translation needs to be *reviewed*</q>
    2. You need to re-start the server if you're using command `compilemessages` :)
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
    - What I assume <small>(do read to the next part!)</small>
      ```bash
      # Follow http://www.i18nguy.com/unicode/language-identifiers.html
      #   1. Way more variations than other settings
      #   2. Use lowercase version instead (zh-hant instead of zh-Hant)
      #   3. Choose the "country-related" one from the list (zh-TW, not zh-Hant)

      # Examples:
      #   de-DE
      #   en-GB  , en-US        
      #   zh-Hant, zh-TW      # single source of true > clarity (eh, actually it's not)
      LANGUAGE_CODE = "en-gb"
      ```
    - *Acutally*
      ```bash
      # Follow https://github.com/django/django/blob/master/django/conf/global_settings.py

      # Simply put, 'LANGUAGE_CODE' MUST conform to the settings in the 'LANGUAGES' (settings.py)
      # Why? Because I tested it out.

      # de      yes, https://github.com/django/django/blob/master/django/conf/global_settings.py#L66
      # de-de   no , https://github.com/django/django/blob/master/django/conf/global_settings.py#L66 doesn't have this
      ```
  - *`LOCALE_PATHS`*
    - What I assume <small>(do read to the next part!)</small>
      ```bash
      # Follow https://github.com/python/cpython/blob/3.6/Lib/locale.py 
      #   1. This setting itself is nothing special
      #   2. The things you need to care about is the sub-directories 🤓
      # Examples:
      #   zh          China with encoding 'eucCN'                 # don't   (too vague) 
      #   zh_cn       China with encoding 'gb2312'                # yes     
      #   zh_cn.euc   China with encoding 'eucCN' (with locale)   # don't   (let user care about the encoding)

      # In practice
      #   these aren't necessarily wrong, but may have issues with third-party library
      #   you just need to met these conditions
      #   - HAVE https://github.com/django/django/blob/master/django/conf/global_settings.py
      #   - HAVE the names in 'LANGUAGES'
      #   - THEN you could use it (replace the  '-' with '_')
      locale/
        zh_tw/
        de_de/
        en_gb/
      ```
    - The settings above works ***until a third-party library was used***, e.g. [`django-rosetta`](https://pypi.org/project/django-rosetta/)
      ```bash
      # Actually it's quite simple since I've made a little research on the source code of 'django-rosetta'.
      # All sub-directories MUST follow the names in the `LANGUAGES` (settings.py)

      # Follow https://github.com/django/django/blob/master/django/conf/global_settings.py
      locale/
        zh_hant/
        de/
        en_gb/
      ```

    - More on *django-rosetta* and *locale names* <small>(all these links directly point to **what I'm trying to say**)</small>
      1. *django-rosetta* source code
        - [find the template that displaying the languages](https://github.com/mbi/django-rosetta/blob/develop/rosetta/templates/rosetta/file-list.html#L23)
        - [find the view that returns the `context` variable](https://github.com/mbi/django-rosetta/blob/develop/rosetta/views.py#L221)
      2. *django-rosetta* documentation
        - [detect languages by what](https://django-rosetta.readthedocs.io/settings.html?highlight=rosetta_languages)
      3. other people's code
        - [a random config of Python Web framework *Saleor*](https://github.com/IsaacMorzy/threads/blob/70d56c1e4a853aab9b91933a1a1a06370763d5cc/.tx/config)
  - Three of them **combined**
    ```bash
    # Examples
    #   ("de", "German")                      de          de/
    #   ("zh-hant", "Traditional Chinese")    zh-hant     zh_hant/
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


### Issues
- About *Django 3.0 compatibility*
  - [*django-parler*](https://pypi.org/project/django-parler/) still only supports `Django <= 3.0.0 `
  - Of course, the *easiest* way is to continue using `Django 2.*.*`, *but*, if you still want to use `3.0`
    ```bash
    # Get the packages which django-parler relies on (choose one)
    # Since Django 3.* already dropped the old `six` module :(
    pip3   install six = "==1.13.0"    # https://pypi.org/project/six/
    pipenv install six = "==1.13.0"

    # Go to the origin
    cd .../YOUR_PYTHON/lib/python3.?/site-packages/parler/  # check by `which python`
    ```
    ```python
    # References
    # ~ https://stackoverflow.com/a/59420098    about `six`
    # ~ https://stackoverflow.com/a/49264381    about `python_2_unicode_compatible`

    # grep -inr 'from django\.utils import six' .
    from django.utils import six  # OLD
    import six                    # NEW

    # grep -inr 'python_2_unicode_compatible' . | grep -v '@\|pyc'
    from django.utils.encoding import force_text, python_2_unicode_compatible  # OLD
    from django.utils.encoding import force_text                               # NEW
    from six import python_2_unicode_compatible                                # NEW
    ```

- Template tag `{% blocktrans %}`
  ```html
  <!-- Do this -->
  {% blocktrans with K=V K=V %} ...
  {% endblocktrans %}

  <!-- Not this -->
  <!-- sometimes the expressions might be really long, well, get with it -->
  {% blocktrans with K=V
                     K=V %} ...
  {% endblocktrans %}
  ```
- pass
