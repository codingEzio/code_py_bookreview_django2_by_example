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
    
    Q: 
    A: 


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

    'social_django',
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
