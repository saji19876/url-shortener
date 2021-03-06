# Django settings for urlweb project.
import os, logging
#from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
)

logging.debug("Reading settings...")
INTERNAL_IPS = ('127.0.0.1',)
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_NAME = os.path.join(PROJECT_PATH, 'database.sqlite')
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
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

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#### CHANGE_ME ####'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.middleware.transaction.TransactionMiddleware',    
    'django_authopenid.middleware.OpenIDMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'urlweb.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates')    
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    #"django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django_authopenid.context_processors.authopenid",
)

AUTH_PROFILE_MODULE = 'shortener.UserProfile'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'urlweb.shortener',
    'registration',
    'django_authopenid',
    'django.contrib.humanize',
    'compress'
)

COMPRESS_CSS_FILTERS = None

STATIC_DOC_ROOT = os.path.join(PROJECT_PATH, 'static')
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = "/account/signin/"
#TEMPLATE_CONTEXT_PROCESSORS += (
#    'django.core.context_processors.request',
#    ) 

SITE_NAME = 'localhost:8000'
SITE_BASE_URL = 'http://' + SITE_NAME + '/'
REQUIRE_LOGIN = True



COMPRESS_CSS = {
    'main': {
        'source_filenames': (
            'css/tskr.us.css',
        ),
        'output_filename': 'css/main_compressed.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'openid': {
        'source_filenames': (
            'css/openid.css',
        ),
        'output_filename': 'css/openid_compressed.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    
    # other CSS groups goes here
}

COMPRESS_JS = {
    'all': {
        'source_filenames': (
            'js/jquery.min.js',
            'js/jquery.tablesorter.min.js',
            'js/openid-jquery.js',
            'js/font/cufon-yui.js',
            'js/font/ChunkFive_400.font.js',
            'js/raphael-min.js',
            'js/g.raphael/g.raphael.js',
            'js/g.raphael/g.bar.js',
            'js/g.raphael/g.dot.js',
            'js/g.raphael/g.line.js',
            'js/g.raphael/g.pie.js',            
        ),
        'output_filename': 'js/all_compressed.js',
    },
    "base":{
        'source_filenames': (
            'js/jquery.min.js',
            'js/jquery.tablesorter.min.js',
            'js/font/cufon-yui.js',
            'js/font/ChunkFive_400.font.js'        
        ),
        'output_filename': 'js/base_compressed.js',
    },
    "openid": {
        'source_filenames': (
            'js/openid-jquery.js',
            'js/base_openid.js'
            
        ),
        'output_filename': 'js/openid_compressed.js',
    },
    "graphing": {
        'source_filenames': (
            'js/raphael-min.js',
            'js/g.raphael/g.raphael.js',
            'js/g.raphael/g.bar.js',
            'js/g.raphael/g.dot.js',
            'js/g.raphael/g.line.js',
            'js/g.raphael/g.pie.js',
        ),
        'output_filename': 'js/graphing_compressed.js',
    },
    "simplegraph": {
        'source_filenames': (
            'js/raphael.js',
            'js/jquery.simplegraph.js',
        ),
        'output_filename': 'js/simplegraph_compressed.js',
    },
    "date_picker": {
        'source_filenames': (
            'js/jquery.ui.core.js',
            'js/jquery.ui.datepicker.js',
            'js/date_base.js'
        ),
        'output_filename': 'js/date_picker_compressed.js',
    },
    "protoviz":{
        'source_filenames':(
            'js/protovis-d3.2.js',
        ),
        'output_filename': 'js/protoviz_compressed.js',
    }
}
COMPRESS = True
COMPRESS_AUTO = True
ACCOUNT_ACTIVATION_DAYS = 5
try:
    from local_settings import *
except ImportError:
    pass
