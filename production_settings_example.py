# Production settings template
# Use environment variables for secure deployment

import os
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# SECURITY WARNING: Update this for production
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') if os.environ.get('ALLOWED_HOSTS') else []

# Generate a new secret key for production
# You can use: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-production-secret-key-here')

# Database for production (update as needed)
if os.environ.get('DATABASE_URL'):
    # For platforms like Heroku that provide DATABASE_URL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    # Manual PostgreSQL configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'portfolio_db'),
            'USER': os.environ.get('DB_USER', 'your_db_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'your_db_password'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }

# Email configuration for production - uses environment variables from settings.py
# No need to override here as settings.py already uses environment variables

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '31536000'))  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
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
