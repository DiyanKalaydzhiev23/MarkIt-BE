import os
import decouple
import cloudinary
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = decouple.config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = [
    os.getenv('HOST', decouple.config('HOST')),
    '127.0.0.1',
    'localhost',
]

CSRF_TRUSTED_ORIGINS = [
    'https://' + os.getenv('HOST', decouple.config('HOST')),
    'http://127.0.0.1:8000',
]

CORS_ORIGIN_WHITELIST = (
    'http://localhost:8000',
    'http://localhost:3000',
    'https://' + os.getenv('HOST', decouple.config('HOST')),
)

CORS_ALLOW_HEADERS = (
    'content-disposition', 'accept-encoding', 'credentials',
    'content-type', 'accept', 'origin', 'authorization', 'Ngrok-Skip-Browser-Warning'
)

MY_APPS = [
    'auth_app',
    'file_upload_router',
    'analyze_file',
    'summary_app',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'rest_framework.authtoken',
    'corsheaders',
] + MY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

ROOT_URLCONF = 'MakeIt.urls'

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

WSGI_APPLICATION = 'MakeIt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DBNAME', decouple.config('DBNAME')),
        'USER': os.getenv('DBUSER', decouple.config('DBUSER')),
        'PASSWORD': os.getenv('DBPASS', decouple.config('DBPASS')),
        'HOST': os.getenv('DBHOST', decouple.config('DBHOST')),
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

CLOUDINARY = {
    'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME', decouple.config('CLOUDINARY_CLOUD_NAME')),
    'api_key': os.getenv('CLOUDINARY_API_KEY', decouple.config('CLOUDINARY_API_KEY')),
    'api_secret': os.getenv('CLOUDINARY_API_SECRET', decouple.config('CLOUDINARY_API_SECRET')),
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "auth_app.User"
