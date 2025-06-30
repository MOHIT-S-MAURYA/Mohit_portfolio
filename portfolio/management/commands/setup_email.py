from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Set up email configuration for contact form'

    def add_arguments(self, parser):
        parser.add_argument('--email', required=True, help='Your email address')
        parser.add_argument('--password', required=True, help='Your email app password')
        parser.add_argument('--provider', default='gmail', choices=['gmail', 'outlook', 'yahoo'], help='Email provider')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        provider = options['provider']
        
        # Email settings based on provider
        if provider == 'gmail':
            host = 'smtp.gmail.com'
            port = 587
        elif provider == 'outlook':
            host = 'smtp-mail.outlook.com'
            port = 587
        elif provider == 'yahoo':
            host = 'smtp.mail.yahoo.com'
            port = 587
        
        # Create local_settings.py file
        local_settings_content = f'''# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '{host}'
EMAIL_PORT = {port}
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '{email}'
EMAIL_HOST_PASSWORD = '{password}'
DEFAULT_FROM_EMAIL = '{email}'
CONTACT_EMAIL = '{email}'
'''
        
        settings_dir = os.path.dirname(settings.__file__)
        local_settings_path = os.path.join(settings_dir, 'local_settings.py')
        
        with open(local_settings_path, 'w') as f:
            f.write(local_settings_content)
        
        self.stdout.write(
            self.style.SUCCESS(f'Email configuration saved to {local_settings_path}')
        )
        self.stdout.write(
            self.style.WARNING('Important: Make sure to use an App Password for Gmail, not your regular password!')
        )
        self.stdout.write(
            self.style.WARNING('For Gmail: Go to Google Account Settings > Security > 2-Step Verification > App passwords')
        )
