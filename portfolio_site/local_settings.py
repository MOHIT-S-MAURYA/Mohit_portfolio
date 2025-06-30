# Email Configuration for Portfolio Site
# 
# INSTRUCTIONS FOR MOHIT:
# 1. Go to: https://myaccount.google.com/security
# 2. Enable "2-Step Verification" if not already enabled
# 3. Find "App passwords" section (only appears after 2FA is enabled)
# 4. Click "App passwords" → Select "Mail" → Click "Generate"
# 5. Copy the 16-character password (like: abcd efgh ijkl mnop)
# 6. Paste it below replacing the empty string

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'msm606248@gmail.com'
EMAIL_HOST_PASSWORD = 'ptgcvnqkjayybgwf'  # ⬅️ NO SPACES - one continuous string
DEFAULT_FROM_EMAIL = 'msm606248@gmail.com'
CONTACT_EMAIL = 'msm606248@gmail.com'

# For testing without real emails (current mode):
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
