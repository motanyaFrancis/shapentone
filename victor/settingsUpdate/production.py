import os
from .aws import *
# Database connection settings
# DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME                     = "https://"
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 1000000
SECURE_FRAME_DENY               = True
SECURE_HSTS_PRELOAD             = True
X_FRAME_OPTIONS                 = False

#MY EMAIL SETTING
# MAILER_EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
#EMAIL_USE_TLS = False
# SENDER_USER = 'noreply'
# EMAIL_DOMAIN = os.environ.get('MAILERTOGO_DOMAIN', 'helpmystudents.com')
# DEFAULT_FROM_EMAIL="@".join([SENDER_USER, EMAIL_DOMAIN])
# EMAIL_USE_SSL= True

X_FRAME_OPTIONS = 'SAMEORIGIN'
CORS_ORIGIN_WHITELIST = (
    'https://fonts.googleapis.com',
    'https://'+AWS_S3_CUSTOM_DOMAIN,
    "https://www.shapentone360.com/",
)

CORS_ALLOWED_ORIGINS = [
    "https://www.shapentone360.com/",
]

CSRF_TRUSTED_ORIGINS = [
    "https://www.shapentone360.com/",
]
