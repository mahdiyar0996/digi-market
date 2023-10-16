from .localsettings import *
from pathlib import Path
import os
from redis import Redis
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-4r9=agvch57*(+l)456=tm57&zb=)lh!q_qm0_qz$(q_^x()+x'


DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'core',
    'products',
    'captcha',
    'allauth',
    'debug_toolbar',
    'rest_framework',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}


AUTH_USER_MODEL = 'users.User'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587 #port 567 gmail
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'mahdiyarsmtp@gmail.com'
EMAIL_HOST_PASSWORD = 'juyzgxxkfkomdjoo'


MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'main.urls'

INTERNAL_IPS = [     #django debug toolbar interal ip address
    # ...
    "127.0.0.1",
    # ...
]

DEBUG_TOOLBAR_PANELS = [        #django debug toolbar panels
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "/templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
LOGIN_REDIRECT_URL = '/profile/'
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'APP': {
            'client_id': '549261432966-2q8kb3oai7l2frj5jb8i82g01sg1ei39.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'


STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = 'static/'

LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'home'
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # 'allauth.account.auth_backends.AuthenticationBackend',
]



WSGI_APPLICATION = 'main.wsgi.application'


DATABASES = {       #DJANGO TARIF DATABASE
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DB_NAME,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "USER": DB_USER,
        "PASSWORD": DB_PASS,
        # 'TIME_ZONE': 'Asia/Tehran'

    }
}


#caching
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,  # seconds  connection timeout
            "SOCKET_TIMEOUT": 5,  # seconds  #read and write timeout
            "IGNORE_EXCEPTIONS": True,     #when redis is down dont raise exception
            "PICKLE_VERSION": -1,

        }
    }
}

DJANGO_REDIS_IGNORE_EXCEPTIONS = True    #when redis is down dont raise exception     for all redis servers
# DJANGO_REDIS_LOGGER = 'some.specified.logger'

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


cache = Redis('127.0.0.1', port=6379, db=1, socket_timeout=5, decode_responses=True )


AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
