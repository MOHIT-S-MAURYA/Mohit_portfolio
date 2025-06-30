# Email Configuration
# Copy this file and rename it to local_settings.py, then fill in your email details

# For Gmail (recommended):
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'your-app-password'  # Gmail App Password (not regular password)
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
CONTACT_EMAIL = 'your-email@gmail.com'  # Where contact messages will be sent

# For other email providers:
# 
# Outlook/Hotmail:
# EMAIL_HOST = 'smtp-mail.outlook.com'
# EMAIL_PORT = 587
# 
# Yahoo:
# EMAIL_HOST = 'smtp.mail.yahoo.com'
# EMAIL_PORT = 587
# 
# Custom SMTP:
# EMAIL_HOST = 'your-smtp-server.com'
# EMAIL_PORT = 587  # or 465 for SSL

# For development/testing (prints emails to console):
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
