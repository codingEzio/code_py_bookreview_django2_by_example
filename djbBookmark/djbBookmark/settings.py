import os
from django.urls import reverse_lazy

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
    
    
----- ----- ----- ----- ----- ----- 

    
Some confusions (beginner-level)
    Q: What does "action" do in the `<form action="{% url 'login' %}" ..`
    A: It defines 'Where to send the form-data when the form is submitted.'
       The process would be like '{% url %}' -> 'route' -> 'view' (checking pwd/name)
    
    Q: What if the value of `<form action..` is "#" or "."?
    A: Both of them (#, .) indicates that your form was sent to the same|current page.
    
    Q: Form and <input> 
    A: Any input inside a form (hidden or not) would be submitted 
       e.g. <input type="hidden" name="my_key" value="1000"> => my_key=1000
    
    Q: What about the `clean_password2` in 'forms.py'
    A: For any fields you wanna clean it by yourself, the fmt looks like 'clean_FIELDNAME()'.
       
       Field validators like 'max_length' should be moved into your 
       `clean_FIELDNAME` func. Also check this out: https://stackoverflow.com/a/4914205/6273859
       
       For those fields who depend on each other, use `clean()` (forms.Form)
       Here: https://docs.djangoproject.com/en/2.2/ref/forms/validation#validating-fields-with-clean

Some confusions (more-advanced level)
    Q: Why use `settings.AUTH_USER_MODEL` instead of `get_user_model()`  (models.py)
    A: The `..AUTH..MODEL` will delay the retrieval until all the apps are loaded.
       In short, the 1st one is safer. (~ https://stackoverflow.com/a/24630589/6273859)


----- ----- ----- ----- ----- ----- 

    
Implementing basic log-in
    0) make sure that your app is in the 'INSTALLED_APPS' & its routes being set
    1) write HTML, that is, login page and related widgets(aka. forms)
    2) write routes for your view
    3) write views  for processing logic & rendering the template

What the heck is `<input ..hidden.. value="{{ next }}">` (registration/login.html)
    Q: More specifically, what is the `{{ next }}`
    A: It was used by '@login_required' and other functions, mainly for "redirecting",
       an example: '/login?next=%2Fdashboard' => after "login", redirect to "dashboard"
       
    Q: In conclusion, why we use the bloody `next`?
    A: 1> we're using Django's default authentication ('login.html' & 'logged_out.html')
       2> we need to redirect to a page after users logged in (for us, it's dashboard.html)
       3> cuz Django use it internally (pls check the src code of `login_required`)
    
    ~ https://www.w3schools.com/tags/att_input_value.asp
    ~ https://stackoverflow.com/questions/3441436/the-next-parameter-redirect-django-contrib-auth-login
    Part of it is related to `@login_required`      ( redirect to {{ next }} )
    Part of it is related to "overriding template"  ( hidden input `value={{next}}` for 'post' )

Implementing login & log-out
    0) still {url+view+template}, plus a little bit conf in the 'settings.py'
    1) get the views (urls.py), plus the routes also being set at the same time
    2) customize templ by creating 'templates/registration/{login,logged_out}.html'
    3) conf(settings.py) => [redirect-to-where, where-to-login, where-to-logout] 
    
    plus
    ~1 write a dashboard page
    ~2 add user's name to the nav-bar after he/she's logged in

Implementing password-reset
    0) configure the email backend (whether it's console or SMTP)
    1) write templates  ( password_reset_????.html, 5 in total )
    2) write routes     ( 1-line: path('', include('django.contrib.auth.urls')) )

Implementing user registration
    0) 'form' and {url+view+template} (heavily depended on Django's `User` model)
    1) write forms      two parts <1>clean pwd2 <2>Meta_plus_modelForm + two password field
    2) write views      either create the user or just display a blank form
    3) write templ      main(initialize the form), done(welcome John)
    4) write routes     just 'register/'

Extending the user model (add 'profile photo' when registering)
    00) the only visible diff is that two fields were added to the "registration page"
    01) conf   media files  MEDIA_URL, MEDIA_ROOT                   settings.py
    02) conf   field pkg    pipenv install Pillow==5.0.1            write this in 'Pipfile' is okay as well
    03) write  routes       static(..MEDIA_URL, ..MEDIA_ROOT)       write this in proj-level urls.py
    04) add    fields       two more fields (date_of_birth, photo)
    05) do     migrations   ./manage.py makemigrations && ./manage.py migrate 
    06) conf   admin        register 'Profile' model see you can see it         (** cannot modify yet **)
    07) write  forms        specifically, the user-info (e.g. fname) and the profile part (d.o.b & photo)
    08) write  templates    initialize those forms
    09) modify views        add `Profile.objects.create(user=new_user)` (a placeholder for future mod)
    10) add    views        add `edit_profile` function (do -> behavior[POST|GET], validation, rendering)    
    11) write  routes       add `edit_profile/` for the view function above     (** now you modify it **)
    
    Note: since we've added new fields to the user model,
          every user we created before will be unable to upload their photo (okay🤯)
          what you should do is to create it directly in the 'Profile' admin page
          
    Simplified version
    <1> proj-url + settings             ->  serving static files
    <2> model + Pipfile + migrations/*  ->  ready for photo profile
    <3> admin                           ->  display at backend
    <4> form + view + url + template    ->  widgets (backend: init,vali,route) (frontend: submit,tip) 

Adding notification message
    view    processing the logic & display msg at the right time
    templ   loop the msges even if there's only one (Q: why? A: ../contrib/messages#message-displaying)

Adding social authentication
    Basic setup
    [01] pipenv install social-auth-app-django==2.1.0
    [02] add 'social-auth/' to project-level urls.py
    [03] add 'social_django' to 'INSTALLED_APPS' (settings.py)
    [04] ./manage.py migrate (to create needed models for social-auth)
    [05] use hosts (127.... mysite.com) or ngrok (ngrok http 8000) for future testing

    STATUS: doesn't have any functionalities yet.

    Recommended articles
    ~ https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html
    ~ https://segmentfault.com/a/1190000000635319


----- ----- ----- ----- ----- ----- 


Q&A for myself ☺️
    Q: How does '..ManyToManyField(.. , .. , ..)' work?
    A: Simply put, you can get data using both sides: 'User.images_liked' & 'Image.users_like'

    Q: Why use multi-line comments in the 'bookmarklet_launcher.js'
    A: The single-line(//) style will comment out our code (=> not working)
    
    Q: Why there's `Math.random()` functions in JavaScript code
    A: To prevent the browser from returning a cached file (src code might change over time!)

    Q: Why use template string (`${VAR}`) in JavaScript code
    A: It's clear and concise, just like the `f{name}` in Python

Implementing the bookmarking feature
    Basic setup
    1. new app          django-admin startapp images THEN add it to 'INSTALLED_APPS'
    2. new model        fields: {title, slug, date, url ..}
    3. do migrations    ./manage.py makemigrations images && ./manage.py migrate (obviously)
    4. admin register

    Adding form (let users be able to submit images) 
    # widgets
        * title         must-have
        * url           users don't have to type this manually
        * description   optional
    # methods
        * clean_url     an extension validating tool (.png .jpg ..)
        * save          be in charge of the whole "saving image" process
        
    Adding view (different behaviors for POST/GET)
    * POST  init form with data -> assign user -> saving -> redirecting
    * GET   init from with data (url: ?..&..) (a bit different from the way we handle 'GET' previously)
    
    Adding template
    * display the form (image, url, description)
    
    Adding routes
    * proj    path('images/', include('images.urls', namespace='images'))
    * app     path('create/', views.image_create, name='create')
    
    # An error'd raised if u submit it, cuz the `get_absolute_url` havn't implemented yet
    # but the image would be saved
    To test it by manually making a 'GET' request
    >>> http://127.0.0.1:8000/images/create/
        ?title=Python%20icon
        &url=https://openwhisk.apache.org/images/runtimes/icon-python-text-color-horz.png

    Adding (core) static files
    * images/static/css/bookmarklet.css     copy-and-paste
    * images/static/css/bookmarklet.js      conf | load -> find -> display | sub 'GET' 
    * /templates/bookmarklet_launcher.js    drag to bookmark bar
    
    Modifying templates
    * /templates/account/dashboard.html     images count & tips for bookmarklet
    
    Now the functionality is implemented, we still need to install a software 
    called 'ngrok' for us to actually test it successfully (https!!!!)
    # basic setup
        $ brew cask install ngrok
        $ ngrok http 8000
    # what we need to change
        ~ bookmarklet_launcher.js  site_url
        ~ bookmarklet.js           site_url
        ~ settings.py              ALLOWED_HOSTS
    # about the testing process
        0. blank                typo!
        1. blank                images might be too small (>= 100x100)
        2. blank                some website's syntax of `img src` is weird (e.g. Bing image)
        2. err loading jQuery   possibly because of the uBlock extension (click twice might work)
    # websites for testing
        ~ https://www.amazon.com/s?k=django&ref=nb_sb_noss
        ~ https://www.imdb.com/title/tt2543312/?ref_=ttfc_fc_tt
        
    Lastly, let's add a detail view for images (no more redirection errors!)
    ~ views         write `image_detail` (get the 'id/slug' gen_ed by JavaScript code)
    ~ urls          form the routes based on 'view'
    ~ models        store those "reversed urls"
    ~ templates     img/title/likes/description     /templates/images/image/detail.html     

Generating thumbnail for uploaded pictures
    Basic setup
    1) pipenv install sorl-thumbnail==12.5.0
    2) add `sorl.thumbnail` to 'INSTALLED_APPS'
    3) run migrations (./manage.py migrate)
    4) replace the original `<img src=.. ..>` with new syntax, done!
    
    To test it
    * pin an image, the newly created/redirected image would be a compressed thumbnail

Implementing the AJAX actions 'like image'
    # Django
    ~ views     do opt on database, return JSON-response
    ~ urls      like/
    
    # Template (JavaScript)
    ~ base.html
        + loading jQuery & js-cookie
        + csrf protection in AJAX requests
        + new block [% domready %} for 'liking image' code
    ~ images/image/detail.html
        + add variable  for 'who liked this picture'
        + add class     for "updating the like count"
        + add button    for "invoking the bottom JS code (then calling view)" & "update the LIKE/UNLIKE"
        + add JS code   modify the `<a>` { access id/action, update data/appearance based on id/action }

Implementing "AJAX ONLY!!" decorator for 'like image' function
    $ proj/common/
        ~ __init__.py         nothing
        ~ decorators.py       "decorated" request.is_ajax()

    $ proj/images/views.py
        >>> from common.decorators import ajax_required
        >>> @ajax_required  # add to the top of the 'image_like' function

Implementing image list (& using AJAX to achieve lazy-loading)
    Interaction between the 'view' and the JS code inside the `{% block domready %}`.
    ~ urls      ''
    ~ views     (0) normally return 8 pics per page (1) scrolling -> ajax loading more
    ~ template  [1] a base 'list_ajax.htm' (thumb, link) [2] a list page plus the {%domready%}

    To test it, do make sure that you have at least 10 pictures pinned,
    since the lowest number for paginator to work is 8. 

Implementing list/detail views for user profiles
    views           user_list, user_detail
    routes          user/  user/<username>/
    templates       list.html, detail.html (templates/account/user/)
    setting conf  
        # another way to achieve `get_absolute_url`  
        # since we don't get to change the `auth.user`, this is the only way
        ABSOLUTE_URL_OVERRIDES = {
            'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])
        }

Implementing user-can-follow-each-other feature
    Base setup
    <1> an intermediate model       Contact -> At when(created) who(user_from) FOLLOWED who(user_to)
    <2> a dynamically added field   Contact <> User { user1.followers.all(), user1.following.all() }
    <3> do migrations for `account` app -> ./manage.py makemigrations account && ./manage.py migrate
    
    Do read the doc to gain more understanding of "M2M in Django"
    ~ https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.ManyToManyField.through

    It's pretty much the same procedures as how we impl the 'image_like'
    # Django
    ~ views     get "param of POST", do opt on database, return JSON-response
    ~ urls      users/follow/   (do put this before the `user/<username>/` (regex))
    
    # Template
    ~ account/user/detail.html
        + add variable  for 'total followers'
        + add class     for "updating the followers count"
        + add button    for "invoking the bottom JS code (then calling view)" & "update the FOLLOW/UNFOLLOW"
        + add JS code   modify the `<a>` { access id/action, update data/appearance based on id/action }


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
    'localhost',
    '127.0.0.1',
    '[::1]',
    'mysite.com',  # add `127.0.0.1 mysite.com` to /etc/hosts
    'ec231e41.ngrok.io',
]

# Application definition

INSTALLED_APPS = [
    'account.apps.AccountConfig',
    'images.apps.ImagesConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'social_django',
    'sorl.thumbnail',
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
        'BACKEND' : 'django.template.backends.django.DjangoTemplates',
        'DIRS'    : [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS' : {
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

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Alternative way to specify an URL for a model (get_absolute_url)

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail',
                                        args=[u.username])
}

# Email

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get("EMAIL_HOST")
# EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
# EMAIL_PORT = os.environ.get("EMAIL_PORT")
# EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")

# We're using authentication views provided by Django

LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

# recommended setting for Social Auth Django
# ~ https://python-social-auth-docs.readthedocs.io/en/latest/configuration/django.html

SOCIAL_AUTH_POSTGRES_JSONFIELD = True
# SOCIAL_AUTH_GOOGLE_OAUTH_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH_KEY')
# SOCIAL_AUTH_GOOGLE_OAUTH_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH_SECRET')
