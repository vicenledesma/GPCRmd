# -*- coding: utf-8 -*-
"""
Django settings for protwis project.
"""

#Defaults
QUERY_CHECK_PUBLISHED = True
FILES_NO_LOGIN = False

#Determine http or https (ssl)
SSL=False

#Settings selection
try:
    from config.settings_local_production import *
except ImportError:
    from config.settings_local_development import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG_TOOLBAR = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'modules.accounts',
    'modules.common',
    'modules.dynadb',
    'modules.home',
    'modules.ligand',
    'modules.protein',
    'modules.residue',
    'modules.structure',
    'modules.view'

]
# INSTALLED_APPS = [
#     'dynadb.apps.DynadbConfig',
#     'accounts.apps.AccountsConfig',
#     'view.apps.ViewConfig',
#     'crossreceptor_analysis.apps.CrossreceptorAnalysisConfig',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'django.contrib.humanize',
#     'sendfile',
#     'rest_framework',
#     'rest_framework_swagger',
#     'common',
#     'api',
#     'news',
#     'pages',
#     'home',
#     'protein',
#     'family',
#     'residue',
#     'alignment',
#     'similaritysearch',
#     'similaritymatrix',
#     'structure',
#     'ligand',
#     'interaction',
#     'mutation',
#     'phylogenetic_trees',
#     'sitesearch',
#     'build_' + SITE_NAME,
#     'construct',
#     'tools',
#     'haystack',
#     'drugs',
#     'graphos',
#     'revproxy',
#     'contact_maps',
#     'covid19',
#     'sc2md',
#     'corplots',
# ]

if DEBUG_TOOLBAR:
    INSTALLED_APPS.append('debug_toolbar')

DEBUG_TOOLBAR_MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware']
    
if not DEBUG_TOOLBAR:
    DEBUG_TOOLBAR_MIDDLEWARE = []
    
MIDDLEWARE = DEBUG_TOOLBAR_MIDDLEWARE+\
    ['django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
]

#['protwis.custom_middlewares.MultipleProxyMiddleware']+\'protwis.custom_middlewares.WsgiLogErrors', 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# Analytics
GOOGLE_ANALYTICS_KEY = False

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/GPCRmd/static'
STATICFILES_DIRS = (os.sep.join([BASE_DIR, "static"]),)
MEDIA_URL = '/files/'
MEDIA_ROOT = '/var/www/GPCRmd/media/files/'
SENDFILE_BACKEND = 'sendfile.backends.xsendfile'

#Search Engine

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/collection_gpcrmd'
    },
}

# Serializer

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


# Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            '/var/www/GPCRmd/templates/'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'config.context_processors.google_analytics'
            ],
        },
    },
]

DEFAULT_AUTO_FIELD="django.db.models.AutoField"

#File settings
MAX_UPLOAD_SIZE=2147483648
DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520
NO_FILE_MAX_POST_SIZE = 52428800
FILE_UPLOAD_TEMP_DIR = "/tmp"
FILE_UPLOAD_PERMISSIONS = 0o660

if DEBUG:
   TEMPLATES[0]['OPTIONS']['debug'] = True
   #VOLVER A PONER EN TRUE


# Debug toolbar
if DEBUG:
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    INTERNAL_IPS = ('10.0.2.2')


# Logging
if DEBUG:
    LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'formatters': {
           'verbose': {
               'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
               'datefmt' : "%d/%b/%Y %H:%M:%S"
           },
       },
       'handlers': {
           'django': {
               'level': 'DEBUG',
               'class': 'logging.FileHandler',
               'filename': 'logs/django.log',
               'formatter': 'verbose'
           },
           'build': {
               'level': 'DEBUG',
               'class': 'logging.FileHandler',
               'filename': 'logs/build.log',
               'formatter': 'verbose'
           },
           'protwis': {
               'level': 'DEBUG',
               'class': 'logging.FileHandler',
               'filename': 'logs/protwis.log',
               'formatter': 'verbose'
           },
       },
       'loggers': {
           'django': {
               'handlers':['django'],
               'propagate': True,
               'level':'DEBUG',
           },
           'build': {
               'handlers': ['build'],
               'level': 'DEBUG',
           },
           'protwis': {
               'handlers': ['protwis'],
               'level': 'DEBUG',
           },
       }
    }

SESSION_ENGINE="django.contrib.sessions.backends.file"

#CACHE
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': CACHE_PATH,
    }
}

#MDSRV
MDSRV_UPSTREAM='http://localhost:8081'

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:memberpage'
LOGOUT_REDIRECT_URL = 'accounts:memberpage'

import mimetypes
mimetypes.add_type('text/x-log; charset=UTF-8', '.log', strict=True)
mimetypes.add_type('chemical/x-mdl-sdfile; charset=UTF-8', '.sdf', strict=True)
mimetypes.add_type(' chemical/x-pdb', '.pdb', strict=True)
mimetypes.add_type('chemical/x-charmm-param', '.prm', strict=True)
mimetypes.add_type('chemical/x-charmm-psf', '.psf', strict=True)

