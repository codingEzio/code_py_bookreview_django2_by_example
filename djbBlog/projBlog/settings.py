import os

NOTES = """
What Django versions should I use?
    Stick with X.2.*, namely Django2.2.* (Long-term support version)
    
What if you have multiple setting files?
    Run `./manage.py runserver localhost:5000 --settings=projBlog.settings`

A not-so-common suggestion for PyCharm users
    Be careful with 'New project -> More settings -> Application name'
    the app being created can't be recognized for later migrating command
    So, do use the normal way to create an app: `./manage.py startapp blog`!
    
About "migrations"
    Show  :: ./manage.py showmigrations                 when in doubt, use it!
    Show  :: ./manage.py sqlmigrate APP_NAME MIG_NAME   underlying SQL code of migration
    Make  :: ./manage.py makemigrations APP_NAME        
    Apply :: ./manage.py migrate
    
There's BIG BIG potentials in the `Meta` class inside those models
    DB table name   <-  db_table = 'post'   (far better than `blog(app)_post(model)`)
    Order by what   <-  ordering = ['-publish',]
    ...

Model(models.py) and Admin(admin.py)
    basic functionality(display)    admin.site.register(Post)
    more control and styling        register by using a decorator, the rest is your job  

The ORM (it's better think them as SQL-equiv-but-in-Python! well.. it IS!)
    [Doc (when in doubt, search the fucking doc)]
        https://docs.djangoproject.com/en/2.0/topics/db/queries#retrieving-objects

    [WHERE]
        https://docs.djangoproject.com/en/2.0/topics/db/queries#field-lookups-intro
        e.g. 
            Post .objects.filter(publish__year=2017)
            Entry.objects.filter(pub_date__range=(start_date, end_date))

    [INSERT]
        e.g.
            inst = MODEL(field=VAL, filed2=VAL..)
            inst.save()
            
            MODEL.objects.create(field=VAL, filed2=VAL..)
        
    [UPDATE]
        e.g.
            inst = MODEL(field=VAL, filed2=VAL..)
            inst.field = NEW_VAL
            inst.save()
            
    [DELETE]
        e.g.
            inst = MODEL.objects.all().filter(slug__contains='yikes')
            inst.delete()
            
Why using "managers"?
    Short answer    readability, convenience
    Long  answer    https://stackoverflow.com/questions/14689237/what-is-a-manager-in-django

Where to put your templates?
    By default, Django looks for `APP/templates/` and `ROOT/templates/`
    You can put all ur stuff in the root-level ones (no need to modify `APP_DIRS`)

Where to put your static files?
    Each app should has its own static-files folder (e.g. APP/static)

The routes (urls.py)
    There's some links weren't supposed to be accessed directly (like "typing manually")
    
    The importance of url routes are beyond the words (e.g. view, model, template)
    [1] view    what u wanna do/achieve     Get data / render templ / passing args
    [2] url     access directly, or not     One for app, one for /ROOT/APP(blog)/url_patterns
    [3] templ   set a base, then derives    Pass(models)/Receive(views) data / static / templtags
    [4] model   more things if for templ    Not much to do initially, but more for templ later :)

    Also, a simple intro about `get_absolute_url`   
    ~ It was trying to use `reverse` to return a (relative) url (e.g. /blog/)
    ~ Passing those args are simply the model itself requires that (aka. 'not for other model')

About adding pagination
    Two parts only: views(Paginator) and templates(previous|next|page_num)
    [1] view        paging data(posts) -> get page num -> get its data (with a bit error handling)
    [2] templates   pagination.html     the PREVIOUS/NEXT part
                    blog/list.html      include the pagination part (XD)

    Y'all need to change the param `with page=posts` to `with page=page_obj` (list.html)
    if you're using class-based views
    
How to safely store sensitive data?
    Quick setup
    [1] pipenv install python-dotenv
    [2] enable it (follow its tutorial) (both are ok: manage.py, settings.py)
    [3] add `.env` to your .gitignore file
    [4] add stuff to ur `.env` file at repo's root folder (done☺️)
    [_] to test it: <1> run Py Console <2> print(os.environ.get('EMAIL_HOST'))

About `related_name` in model's Fk/M2M fields definition
    // Post.comments    the comments of a post
    // Comment.post     the post being commented
    class Comment(models.Model):
        post = models.ForeignKey(Post,
                                 on_delete=models.CASCADE,
                                 related_name='comments')

Two ways to build a form
    1) forms.Form       Handwritten         can be though as a HTML snippet
    2) forms.ModelForm  Based on DB model   Django auto-create the widgets for you

Adding tags using 'django_taggit'
    Basic setup
    [1] pipenv install django_taggit==0.22.2
    [2] add `taggit` to 'INSTALLED_APPS' (& some tweaks, like `TAGGIT_CASE_INSENSITIVE = True`)
    [3] add `tags = TaggableManager()` to our model `Post`
    [4] make migrations (since it's tightly related to our models) (e.g. djmakemig blog && djmig)

Recommending similar posts (based on tags)
    Rough steps
    [1] get IDs of those tags
    [2] get posts with the same ID (exclude the current post)
    [3] get the tag with the most occurrences then order by 'publish' (DESC) (:4) 

Adding custom template tag (e.g. {% tag %}
    [1] create dir/file: YOUR_APP/templatetags/{__init__.py, YOUR_TAG.py}
    [2] 
        // Simple tag     --  simply return the result
        // Inclusion tag  --  display the data by rendering another template
        
        @register.simple_tag()
        def get_most_commented_posts(DEFAULT_VALUE_IF_WE_NEED):
            return .. QUERYSET ..
        
        @register.inclusion_tag(TEMPLATE_FILE)
        def show_latest_posts(DEFAULT_VALUE_IF_WE_NEED):
            .. QUERYSET ..
            return { 'USE_IN_TEMPLATE': VAR_WOULD_BE_USED_IN_TEMPLATE }
    
    [3] you can always give the decorator `name='most_commented_posts' as an alias
    [4] load it in your template `{% load TAG from TAG_FILE %}` (u can use it in any templates!)

Adding custom template filter (e.g. {% XXX|filter|filter %}
    Markdown syntax setup (backend)
    [1] pipenv install Markdown==2.6.11
    [2] use it in the same file where the template tags live (=> @register.filter)
    [3] load & add it in the templates

Adding sitemap
    Basic setup
    [1] add 'django.contrib.{sites, sitemaps}' to 'INSTALLED_APPS'
    [2] run './manage.py migrate' since the data needs to be stored in the DB
    [3] add 'sitemaps.py' under your app (override stuff by inheriting `Sitemap`)
    [4] add routes to your 'PROJECT/urls.py'
    [5] add domain name at 'http://localhost:8000/admin/sites/site/' (e.g. localhost:8000)
    [_] to test it: access 'localhost:8000/sitemap.xml'
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2cg#d=s_(tv72z#o+4*j^^y194hg-yh-&l3dc&peeqs!^wrq=x'

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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.sitemaps',

    'blog.apps.BlogConfig',

    'taggit',
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

ROOT_URLCONF = 'projBlog.urls'

TEMPLATES = [
    {
        'BACKEND' : 'django.template.backends.django.DjangoTemplates',
        'DIRS'    : [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'projBlog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME'  : os.path.join(BASE_DIR, 'db.sqlite3'),
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

# Email setup

# You'll need more than this, the rest of them were stored in the .env file
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Third-party library settings
TAGGIT_CASE_INSENSITIVE = True
