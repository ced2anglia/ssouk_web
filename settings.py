# Django settings for ssouk_web project.

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE' : 'django.contrib.gis.db.backends.postgis',
        'NAME': 'geodatabase',
        'USER': 'geouser',
        'PASSWORD': 'geopassword',
    }
}


MEDIA_BUNDLES = (
    # CSS
    ('screen.css',
        #'sass/screen.sass'
        'css/screen.css'
     ),
    ('print.css',
       # 'sass/print.sass',
        'css/print.css',
     ),
    ('ie.css',
        #'sass/ie.sass'
        'css/ie.css'
    ),
                 
    # JS
    ('main.js',
        #'js/jquery-1.5.2.min.js',
        'js/jquery-1.6.min.js',
        
        # Javascript for the map app
        'js/map.js',
    ),
)

# Get project root folder
_project_root = os.path.dirname(__file__)

# Set global media search paths
GLOBAL_MEDIA_DIRS = (
    os.path.join(_project_root, 'static'),
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Set media URL (important: don't forget the trailing slash!).
# PRODUCTION_MEDIA_URL is used when running manage.py generatemedia
MEDIA_DEV_MODE = DEBUG
DEV_MEDIA_URL = '/devmedia/'
PRODUCTION_MEDIA_URL = '/media/'

# Configure yuicompressor if available
YUICOMPRESSOR_PATH = os.path.join(
    os.path.dirname(_project_root), 'yuicompressor.jar')
if os.path.exists(YUICOMPRESSOR_PATH):
    ROOT_MEDIA_FILTERS = {
        'js': 'mediagenerator.filters.yuicompressor.YUICompressor',
        'css': 'mediagenerator.filters.yuicompressor.YUICompressor',
    }
    
ADMIN_MEDIA_PREFIX = '/media/admin/'

    
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'id_fbqde55y5oev3ao(h^myql*%w*bb%o+hvxd0_t2c5%z550s'

# List of callables that know how to import templates from various sources.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.request',
)

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

MIDDLEWARE_CLASSES = (
    'mediagenerator.middleware.MediaMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    
    # 3rd apps
    'mediagenerator',
    
    # Our apps
    'apps.inventory',
    'apps.map'
    
    
)


# Email
# run "python -m smtpd -n -c DebuggingServer localhost:1025" to see outgoing
# messages dumped to the terminal
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = 'do.not.reply@sustainablesouk.com'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
