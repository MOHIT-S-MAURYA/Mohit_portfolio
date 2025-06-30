from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test email configuration by sending a test email'

    def add_arguments(self, parser):
        parser.add_argument('--to', required=True, help='Email address to send test email to')

    def handle(self, *args, **options):
        to_email = options['to']
        
        try:
            send_mail(
                'Test Email from Portfolio Site',
                'This is a test email to verify your email configuration is working correctly.',
                settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                [to_email],
                fail_silently=False,
            )
            self.stdout.write(
                self.style.SUCCESS(f'Test email sent successfully to {to_email}!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to send email: {e}')
            )
            self.stdout.write(
                self.style.WARNING('Please check your email configuration in settings.py or local_settings.py')
            )
