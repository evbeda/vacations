from .base import *  # noqa
import dj_database_url

ALLOWED_HOSTS = [
    'vacationsqa.herokuapp.com',
    'evb-vacations-qa.herokuapp.com',
    'evb-vacations.herokuapp.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vacations',
        'USER': 'name',
        'PASSWORD': '',
        'PORT': '',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static_prod')

INSTALLED_APPS += [  # noqa
    'whitenoise.runserver_nostatic'
]

MIDDLEWARE += [  # noqa
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DB_FROM_ENV = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(DB_FROM_ENV)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

DEBUG = False
