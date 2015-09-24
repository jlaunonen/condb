# encoding: utf-8
from __future__ import absolute_import

import os
from datetime import datetime, timedelta

from django.utils.translation import ugettext_lazy as _

import django.conf.global_settings as defaults


def mkpath(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', *parts))


MKPATH = mkpath

DEBUG = True
TEMPLATE_DEBUG = DEBUG

if DEBUG:
    # XXX Monkey patch is_secure_transport to allow development over insecure HTTP

    from warnings import warn
    warn(UserWarning("Monkey_patching oauthlib.oauth2:is_secure_transport to allow OAuth2 over HTTP. Never do this in production!"))

    fake_is_secure_transport = lambda token_url: True

    import oauthlib.oauth2
    import requests_oauthlib.oauth2_session
    import oauthlib.oauth2.rfc6749.parameters
    import oauthlib.oauth2.rfc6749.clients.base

    for module in [
        oauthlib.oauth2,
        requests_oauthlib.oauth2_session,
        oauthlib.oauth2.rfc6749.parameters,
        oauthlib.oauth2.rfc6749.clients.base,
    ]:
        module.is_secure_transport = fake_is_secure_transport

CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_URLS_REGEX = r'^/(api|oauth2)/.*$'
CORS_ORIGIN_WHITELIST = (
    # Add any applications that need CORS for the API here
    # 'kirppu.tracon.fi',
)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'turska.sqlite3',                      # Or path to database file if using sqlite3.
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Uncomment if you have memcached
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': [
#             '127.0.0.1:11211'
#         ]
#     }
# }

ALLOWED_HOSTS = []

TIME_ZONE = 'Europe/Helsinki'
DATETIME_FORMAT = SHORT_DATETIME_FORMAT = 'd.m.Y H:i'
LANGUAGE_CODE = 'fi-FI'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = mkpath('media')
MEDIA_URL = '/media/'
STATIC_ROOT = mkpath('static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'jhdjl*kxcet2aaz)%ixmois*j_p+d*q79%legoz+9el(c%zc$%'

TEMPLATE_LOADERS = (
    ('pyjade.ext.django.Loader',(
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'core.middleware.PageWizardMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'turska.urls'
WSGI_APPLICATION = 'turska.wsgi.application'
APPEND_SLASH = False

TEMPLATE_DIRS = (
    mkpath('turska','templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = defaults.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'core.context_processors.core_context',
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'pyjade',
    'crispy_forms',
    'oauth2_provider',

    'core',
    'programme',
    'labour',
    'labour_common_qualifications',
    'tickets',
    'payments',
    'mailings',
    'api',
    'api_v2',
    'badges',
    'access',
    'nexmo',
    'sms',

    # Uncomment if you have IPA
    #'external_auth',

    # Uncomment if you do PDF tickets
    'lippukala',

    # Uncomment if you have Celery
    # 'background_tasks',

    'branding',
    'desuprofile_integration',

    'events.tracon8',
    'events.tracon9',
    'events.kawacon2014',
    'events.concon9',
    'events.traconx',
    'events.hitpoint2015',
    'events.yukicon2015',
    'events.kuplii2015',
    'events.popcult2015',
    'events.mimicon2015',
    'events.animecon2015',
    'events.popcultday2015',
    'events.yukicon2016',
    'events.finncon2016',
    'events.frostbite2016',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': True
        },
        'kompassi': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': True
        },
    }
}

LOGIN_URL = '/login'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

DATE_FORMAT = 'j.n.Y'
DATE_FORMAT_STRFTIME = '%d.%m.%Y'

DATETIME_FORMAT = 'j.n.Y G:i:s'
DATETIME_FORMAT_STRFTIME = '%d.%m.%Y %H:%M:%S'

LANGUAGES = (
    ('fi', _('Finnish')),
    ('en', _('English')),
    # and all the other languages you have translated.
)

LANGUAGE_CODE = 'fi'  # or which language you want to use.

USE_L10N = True
USE_L18N = True

KOMPASSI_APPLICATION_NAME = u'Kompassi'
KOMPASSI_INSTALLATION_NAME = u'Kompassi (DEV)'
KOMPASSI_INSTALLATION_NAME_ILLATIVE = u'Kompassin kehitysinstanssiin'
KOMPASSI_INSTALLATION_NAME_GENITIVE = u'Kompassin kehitysinstanssin'
KOMPASSI_INSTALLATION_SLUG = 'turskadev'
KOMPASSI_PRIVACY_POLICY_URL = 'http://media.tracon.fi/2014/tracon9_turska_rekisteriseloste.pdf'

AUTHENTICATION_BACKENDS = (
    'core.backends.KompassiImpersonationBackend',
    'django.contrib.auth.backends.ModelBackend',
)


# These MUST match those in IPA
KOMPASSI_PASSWORD_MIN_LENGTH = 8
KOMPASSI_PASSWORD_MIN_CLASSES = 3

# Don't actually send email
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
DEFAULT_FROM_EMAIL = 'suunnistajat@kompassi.eu'


if 'external_auth' in INSTALLED_APPS:
    # in case of emergency, break glass
    if DEBUG:
        import logging

        logger = logging.getLogger('django_auth_ldap')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)

    AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
    ) + AUTHENTICATION_BACKENDS

    KOMPASSI_LDAP_DOMAIN = 'dc=tracon,dc=fi'
    KOMPASSI_LDAP_USERS = 'cn=users,cn=accounts,{KOMPASSI_LDAP_DOMAIN}'.format(**locals())
    KOMPASSI_LDAP_GROUPS = 'cn=groups,cn=accounts,{KOMPASSI_LDAP_DOMAIN}'.format(**locals())

    KOMPASSI_IPA_JSONRPC = 'https://moukari.tracon.fi/ipa/json'
    KOMPASSI_IPA_CACERT_PATH = '/etc/ipa/ca.crt'

    import ldap
    from django_auth_ldap.config import LDAPSearch, PosixGroupType, NestedGroupOfNamesType

    #AUTH_LDAP_SERVER_URI = "ldaps://moukari.tracon.fi"
    AUTH_LDAP_SERVER_URI = "ldaps://localhost:64636"

    # AUTH_LDAP_BIND_DN = ""
    # AUTH_LDAP_BIND_PASSWORD = ""
    # AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,{KOMPASSI_LDAP_USERS}".format(**locals())
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        KOMPASSI_LDAP_USERS,
        ldap.SCOPE_SUBTREE,
        "(uid=%(user)s)"
    )
    AUTH_LDAP_ALWAYS_UPDATE_USER = True

    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
        KOMPASSI_LDAP_GROUPS,
        ldap.SCOPE_SUBTREE,
        "(objectClass=groupOfNames)"
    )
    AUTH_LDAP_GROUP_TYPE = NestedGroupOfNamesType()
    AUTH_LDAP_MIRROR_GROUPS = True

    AUTH_LDAP_REQUIRE_GROUP = "cn={KOMPASSI_INSTALLATION_SLUG}-users,{KOMPASSI_LDAP_GROUPS}".format(**locals())
    # AUTH_LDAP_DENY_GROUP = "cn={KOMPASSI_INSTALLATION_SLUG}-banned,{KOMPASSI_LDAP_GROUPS}".format(**locals())

    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        "is_active": "cn={KOMPASSI_INSTALLATION_SLUG}-users,{KOMPASSI_LDAP_GROUPS}".format(**locals()),
        "is_staff": "cn={KOMPASSI_INSTALLATION_SLUG}-staff,{KOMPASSI_LDAP_GROUPS}".format(**locals()),
        "is_superuser": "cn={KOMPASSI_INSTALLATION_SLUG}-admins,{KOMPASSI_LDAP_GROUPS}".format(**locals()),
    }

    AUTH_LDAP_USER_ATTR_MAP = {"first_name": "givenName", "last_name": "sn"}
    AUTH_LDAP_GLOBAL_OPTIONS = {
        ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_ALLOW,
        ldap.OPT_X_TLS_CACERTFILE: KOMPASSI_IPA_CACERT_PATH,
           ldap.OPT_REFERRALS: 0,
    }

    from sets import Set
    KOMPASSI_NEW_USER_INITIAL_GROUPS = Set([
        "{KOMPASSI_INSTALLATION_SLUG}-users".format(**locals()),

        # to make sure users created via turskadev.tracon.fi can also access the
        # actual installation
        'turska-users',
    ])


if 'payments' in INSTALLED_APPS:
    from payments.defaults import CHECKOUT_PARAMS


if 'lippukala' in INSTALLED_APPS:
    import tickets.lippukala_integration

    LIPPUKALA_PREFIXES = tickets.lippukala_integration.PREFIXES
    LIPPUKALA_LITERATE_KEYSPACES = tickets.lippukala_integration.KEYSPACES

    LIPPUKALA_CODE_MIN_N_DIGITS = 7
    LIPPUKALA_CODE_MAX_N_DIGITS = 7

    # NOTE these will be overridden by the respective fields in TicketsEventMeta
    # however, they need to be defined in settings or lippukala will barf.
    LIPPUKALA_PRINT_LOGO_PATH = mkpath('events', 'popcult2015', 'static', 'images', 'popcult.png')
    LIPPUKALA_PRINT_LOGO_SIZE_CM = (3.0, 3.0)


if 'background_tasks' in INSTALLED_APPS:
    BROKER_URL = 'amqp://{KOMPASSI_INSTALLATION_SLUG}:{KOMPASSI_INSTALLATION_SLUG}@localhost/{KOMPASSI_INSTALLATION_SLUG}'.format(**locals())
    CELERY_ACCEPT_CONTENT = ['json']

    #EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

    CELERY_SEND_TASK_ERROR_EMAILS = not DEBUG
    SERVER_EMAIL = DEFAULT_FROM_EMAIL

    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'


if 'api' in INSTALLED_APPS:
    KOMPASSI_APPLICATION_USER_GROUP = '{KOMPASSI_INSTALLATION_SLUG}-apps'.format(**locals())


if 'api_v2' in INSTALLED_APPS:
    AUTHENTICATION_BACKENDS = (
        'oauth2_provider.backends.OAuth2Backend',
    ) + AUTHENTICATION_BACKENDS

    OAUTH2_PROVIDER = dict(
        SCOPES=dict(
            read=u'Tietää nimesi, sähköpostiosoitteesi, puhelinnumerosi ja syntymäaikasi',
            write=u'Muokata käyttäjä- ja henkilötietojasi',
        )
    )


if 'nexmo' in INSTALLED_APPS:
    NEXMO_USERNAME = 'username'
    NEXMO_PASSWORD = 'password'
    NEXMO_FROM = 'Name or number'
    NEXMO_INBOUND_KEY = '0123456789abcdef'


if 'branding' in INSTALLED_APPS:
    KOMPASSI_ACCOUNT_BRANDING = u'Kompassi-tunnus'
    KOMPASSI_ACCOUNT_BRANDING_PARTITIVE = u'Kompassi-tunnusta'
    KOMPASSI_ACCOUNT_BRANDING_GENITIVE = u'Kompassi-tunnuksen (ent. Tracon-tunnuksen)'
    KOMPASSI_ACCOUNT_BRANDING_ADESSIVE = u'Kompassi-tunnuksella'
    KOMPASSI_ACCOUNT_BRANDING_2ND_PERSON_ADESSIVE = u'Kompassi-tunnuksellasi'


if 'desuprofile_integration' in INSTALLED_APPS:
    KOMPASSI_DESUPROFILE_HOST = 'https://desucon.fi'
    KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_ID = 'kompassi_insecure_client_id'
    KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_SECRET = 'kompassi_insecure_client_secret'
    KOMPASSI_DESUPROFILE_OAUTH2_SCOPE = ['read']
    KOMPASSI_DESUPROFILE_OAUTH2_AUTHORIZATION_URL = '{KOMPASSI_DESUPROFILE_HOST}/oauth2/authorize/'.format(**locals())
    KOMPASSI_DESUPROFILE_OAUTH2_TOKEN_URL = '{KOMPASSI_DESUPROFILE_HOST}/oauth2/token/'.format(**locals())
    KOMPASSI_DESUPROFILE_API_URL = '{KOMPASSI_DESUPROFILE_HOST}/api/user/me/'.format(**locals())
