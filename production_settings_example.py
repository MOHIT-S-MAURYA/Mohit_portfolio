# Production settings template
# Copy this file to local_settings.py and update values for production

import os
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: Update this for production
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Generate a new secret key for production
# You can use: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY = 'your-production-secret-key-here'

# Database for production (update as needed)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'portfolio_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Email configuration for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
CONTACT_EMAIL = 'your-email@gmail.com'

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Static files for production
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files for production (consider using cloud storage)
MEDIA_ROOT = BASE_DIR / 'media'

# Logging for production
LOGGING['handlers']['file']['filename'] = '/var/log/django/portfolio.log'  # Update path as needed
LOGGING['loggers']['django']['level'] = 'WARNING'
LOGGING['loggers']['portfolio']['level'] = 'INFO'

# Admin emails for error reporting
ADMINS = [
    ('Your Name', 'your-email@example.com'),
]
MANAGERS = ADMINS

# Cache configuration (optional)
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#     }
# }
