import os
from pathlib import Path

import environ
from decouple import config
from django.contrib.messages import constants as messages

# Initialise environment variables
env = environ.Env()
environ.Env.read_env(".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
LOGGING_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOGGING_DIR, "django.log"),
        },
         "payment": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOGGING_DIR, "payment.log"),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
        # "selfservice": {
        #     "handlers": ["file"],
        #     "level": "DEBUG",
        #     "propagate": True,
        # },
        "payment": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
# 3u1Ic7GElb1SPO50oh

try:
    SECRET_KEY = config("SECRET_KEY")
except KeyError as e:
    raise RuntimeError("Could not find a SECRET_KEY in environment") from e

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", ".shapentone360.com", "https://www.shapentone360.com",".63.250.33.253"]


# CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 1000000
SECURE_FRAME_DENY = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = False

X_FRAME_OPTIONS = "SAMEORIGIN"

CSRF_TRUSTED_ORIGINS = [
    "https://www.shapentone360.com",
    "https://7221-41-139-164-167.ngrok-free.app",
]


CORS_ORIGIN_WHITELIST = [
    "https://fonts.googleapis.com",
    # Daraja Call back IPs
    "https://196.201.214.200",
    "https://196.201.214.206",
    "https://196.201.213.114",
    "https://196.201.214.207",
    "https://196.201.214.208",
    "https://196.201.213.44",
    "https://196.201.212.127",
    "https://196.201.212.128",
    "https://196.201.212.129",
    "https://196.201.212.136",
    "https://196.201.212.74",
    "https://196.201.212.69",
    # Host Callback IPs
    "https://www.shapentone360.com",
]


CORS_ALLOWED_ORIGINS = [
    # Host Callback IPs
    "https://www.shapentone360.com",
]

# Application definition

# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',  # existing backend
#     'allauth.account.auth_backends.AuthenticationBackend',
# )

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party applications
    "corsheaders",
    "drf_spectacular",
    "crispy_forms",
    "crispy_bootstrap5",
    'tinymce',
    'storages',
    'pwa',
    'subscriptions',
    'sorl.thumbnail',
    'django_recaptcha',
    
    # myApps
    "authentication",
    "base",
    "dashboard",
    "payment",
    "setup",
    "articles",
    "myRequest",
    # # 3rd party authentication
    # 'django.contrib.sites',  # make sure sites is included
]

SITE_ID = 1
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "victor.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates", "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']

DATE_INPUT_FORMATS = ["%d-%m-%Y"]

WSGI_APPLICATION = "victor.wsgi.application"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": "5432",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# configuring the location for media
MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = "/var/www/shapentone360.com/static"
# MEDIA_ROOT = '/var/www/shapentone360.com/media'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = "authentication.NewUser"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field


MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 5 MB

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = 'shapentone360@gmail.com'
EMAIL_HOST_PASSWORD = 'wdipkrbgdmscaehb'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'shapentone360@gmail.com'


LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/login/"

# Set your currency type
DFS_CURRENCY_LOCALE = "en_us"

# Specify your base template file
DFS_BASE_TEMPLATE = "base.html"

TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | blocks fontfamily styles fontsizeselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent | lineheight numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    # To force a specific language instead of the Django current language.
    "language": "en",
    "font_formats": 'montserrat,"Open Sans",Arial,sans-serif',
    "icons": "material",
}
TINYMCE_SPELLCHECKER = True


PWA_APP_NAME = "Victor Fitness"
PWA_APP_DESCRIPTION = "Victor Fitness App"
PWA_APP_THEME_COLOR = "#0A0302"
PWA_APP_BACKGROUND_COLOR = "#ffffff"
PWA_APP_DISPLAY = "standalone"
PWA_APP_SCOPE = "/"
PWA_APP_ORIENTATION = "any"
PWA_APP_START_URL = "/"
PWA_APP_STATUS_BAR_COLOR = "default"
PWA_APP_ICONS = [{"src": "/static/logo/favicon.png", "sizes": "160x160"}]
PWA_APP_ICONS_APPLE = [{"src": "/static/logo/favicon.png", "sizes": "160x160"}]
PWA_APP_SPLASH_SCREEN = [
    {
        "src": "/static/logo/splash.png",
        "media": "(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)",
    }
]
PWA_APP_DIR = "ltr"
PWA_APP_LANG = "en-US"
PWA_APP_SHORTCUTS = [
    {
        "name": "Shortcut",
        "url": "/target",
        "description": "Shortcut to a page in my application",
    }
]
PWA_APP_SCREENSHOTS = [
    {"src": "/static/logo/splash.png", "sizes": "750x1334", "type": "image/png"}
]


MPESA_CONSUMER_KEY = config("MPESA_CONSUMER_KEY")
MPESA_CONSUMER_SECRET = config("MPESA_CONSUMER_SECRET")
MPESA_EXPRESS_SHORTCODE = config("MPESA_EXPRESS_SHORTCODE")
MPESA_PASSKEY = config("MPESA_PASSKEY")
BUSINESS_SHORTCODE = config("BUSINESS_SHORTCODE")


# RECAPTCHA_PUBLIC_KEY = config("RECAPTCHA_PUBLIC_KEY ")
# RECAPTCHA_PRIVATE_KEY = config("RECAPTCHA_PRIVATE_KEY ")
# RECAPTCHA_DOMAIN = 'www.google.com'
# RECAPTCHA_PROXY = {'http': 'http://127.0.0.1:8100', 'https': 'https://127.0.0.1:8100'}

RECAPTCHA_PUBLIC_KEY = '6LdwEN0pAAAAAPkj7Sv1rqKCoUVFewKF0fH4D93C'
RECAPTCHA_PRIVATE_KEY = '6LdwEN0pAAAAAA5vJEzCVaVHScECXOGqzQGsLDfq'
