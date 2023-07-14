from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = (
    'django-insecure-!ib8d!h8@wz(2j%g^#o(v-l#y$$ivu26i*md&1$%9$4xy31wb+'
)

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'djoser',
    'users',
    'recipes',
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

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase_two',
        'USER': 'postgres',
        'PASSWORD': 'uFB&kDZ*t#L^3J2q4kS4rnr*NRfR@q',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'
REST_FRAMEWORK = {
    'DJANGO_SETTINGS_MODULE': 'backend.settings',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'backend.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 6,
}

DJOSER = {
    'HIDE_USERS': False,
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'user_create': 'users.serializers.CustomUserCreateSerializer',
        'user': 'users.serializers.CustomUserSerializer',
        'current_user': 'users.serializers.CustomUserSerializer',
    },
    'PERMISSIONS': {
        'user_list': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
        'user': ['rest_framework.permissions.IsAuthenticated'],
    },
}
# --------------------------------------------------------------- #
# Июзернэймы, запрещенные к регистрации для пользователей системы #
# --------------------------------------------------------------- #
FORBIDDEN_USERNAMES = ['me', 'admin', 'superuser']

# --------------------------------------------------------------- #
# Длины полей, используемых в моделях приложений users и recipes  #
# --------------------------------------------------------------- #
MAX_USERNAME_LENGTH = 150
MAX_FIRST_NAME_LENGTH = 150
MAX_LAST_NAME_LENGTH = 150
MAX_PASSWORD_NAME_LENGTH = 150
MAX_INGREDIENT_NAME_LENGTH = 200
MAX_INGREDIENT_MEASUREMENT_UNIT_LENGTH = 200
MAX_TAG_NAME_LENGTH = 50
MAX_TAG_COLOR_LENGTH = 7
MAX_RECIPE_NAME_LENGTH = 200
MIN_COOKING_TIME = 1
MAX_COOKING_TIME = 20161
MIN_AMOUNT = 1
MAX_AMOUNT = 10000
