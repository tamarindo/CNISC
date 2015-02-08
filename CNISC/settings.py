
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '614+m4hd)64isqk#s%9*-4z)uvtumlnj&12ebqpwp15p4%249r'

try:
    from .local_settings import DEBUG , TEMPLATE_DEBUG
except Exception:
    DEBUG = True
    TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

APPS = ["apps.main",
        "apps.messaging",
        "apps.userManager",
        "apps.tags",
        "apps.oauthSocial",
        "apps.parceadores",
        ]
try:
    import django_extensions
    APPS += ["django_extensions"]
except:
    pass

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_wysiwyg',
    'django_facebook', 
) + tuple(APPS)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'CNISC.urls'

WSGI_APPLICATION = 'CNISC.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
    ),
}


try:
    from .local_settings import DATABASES
except Exception, e:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'UTC'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_DIRS = ( os.path.join (BASE_DIR,'public/static'), )
MEDIA_ROOT = ( os.path.join (BASE_DIR,'public/media') )

STATIC_URL= '/static/'
MEDIA_URL = '/media/'

# configuracion para el modulo de wysiwyg

DJANGO_WYSIWYG_FLAVOR = 'ckeditor' 
DJANGO_WYSIWYG_MEDIA_URL = STATIC_URL + "libs/ckeditor/" 



FACEBOOK_APP_ID = '367234420120488'
FACEBOOK_APP_SECRET =  'b809dcbd4b3aa24008e73a87626020e3'