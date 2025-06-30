from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxLengthValidator, MinLengthValidator
from django.utils.html import strip_tags
import re
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Enhanced contact form with comprehensive validation and security measures.
    """
    
    # Custom validators
    name_validator = RegexValidator(
        regex=r'^[a-zA-Z\s\'.-]+$',
        message='Name can only contain letters, spaces, apostrophes, periods, and hyphens.'
    )
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'maxlength': 100,
                'required': True,
                'autocomplete': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'maxlength': 254,
                'required': True,
                'autocomplete': 'email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief subject of your message',
                'maxlength': 200,
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your message... (Please be as detailed as possible)',
                'rows': 6,
                'maxlength': 2000,
                'required': True
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom validators to fields
        self.fields['name'].validators.append(self.name_validator)
        self.fields['name'].validators.append(MinLengthValidator(2, 'Name must be at least 2 characters long.'))
        self.fields['subject'].validators.append(MinLengthValidator(5, 'Subject must be at least 5 characters long.'))
        self.fields['message'].validators.append(MinLengthValidator(10, 'Message must be at least 10 characters long.'))
        
        # Set help text
        self.fields['name'].help_text = 'Enter your full name (2-100 characters)'
        self.fields['email'].help_text = 'A valid email address where I can reach you'
        self.fields['subject'].help_text = 'Brief description of your inquiry (5-200 characters)'
        self.fields['message'].help_text = 'Detailed message about your project or inquiry (10-2000 characters)'

    def clean_name(self):
        """Custom validation for name field."""
        name = self.cleaned_data.get('name', '').strip()
        
        if not name:
            raise ValidationError('Name is required.')
        
        # Remove extra whitespace
        name = ' '.join(name.split())
        
        # Check for minimum length after cleaning
        if len(name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')
        
        # Check for maximum length
        if len(name) > 100:
            raise ValidationError('Name must be less than 100 characters long.')
        
        # Check for invalid characters (more strict)
        if not re.match(r'^[a-zA-Z\s\'.-]+$', name):
            raise ValidationError('Name contains invalid characters. Only letters, spaces, apostrophes, periods, and hyphens are allowed.')
        
        # Check for consecutive spaces or special characters
        if re.search(r'[\s\'-\.]{2,}', name):
            raise ValidationError('Name cannot contain consecutive spaces or special characters.')
        
        # Check for names that are too short or suspicious
        if len(name.replace(' ', '')) < 2:
            raise ValidationError('Please enter a valid name.')
        
        return name

    def clean_email(self):
        """Custom validation for email field."""
        email = self.cleaned_data.get('email', '').strip().lower()
        
        if not email:
            raise ValidationError('Email is required.')
        
        # Additional email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValidationError('Please enter a valid email address.')
        
        # Check for common suspicious patterns
        suspicious_patterns = [
            r'test@test\.com',
            r'example@example\.com',
            r'admin@admin\.com',
            r'[0-9]{10,}@',  # Too many consecutive numbers
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, email, re.IGNORECASE):
                raise ValidationError('Please enter a real email address.')
        
        return email

    def clean_subject(self):
        """Custom validation for subject field."""
        subject = self.cleaned_data.get('subject', '').strip()
        
        if not subject:
            raise ValidationError('Subject is required.')
        
        # Remove extra whitespace
        subject = ' '.join(subject.split())
        
        if len(subject) < 5:
            raise ValidationError('Subject must be at least 5 characters long.')
        
        if len(subject) > 200:
            raise ValidationError('Subject must be less than 200 characters long.')
        
        # Check for spam-like patterns
        spam_patterns = [
            r'urgent.{0,20}response',
            r'business.{0,20}proposal',
            r'million.{0,20}dollar',
            r'click.{0,20}here',
            r'free.{0,20}money',
            r'congratulations',
            r'lottery',
            r'winner',
        ]
        
        for pattern in spam_patterns:
            if re.search(pattern, subject, re.IGNORECASE):
                raise ValidationError('Subject appears to be spam. Please use a different subject.')
        
        # Remove HTML tags if present
        subject = strip_tags(subject)
        
        return subject

    def clean_message(self):
        """Custom validation for message field."""
        message = self.cleaned_data.get('message', '').strip()
        
        if not message:
            raise ValidationError('Message is required.')
        
        if len(message) < 10:
            raise ValidationError('Message must be at least 10 characters long.')
        
        if len(message) > 2000:
            raise ValidationError('Message must be less than 2000 characters long.')
        
        # Check for excessive repetition
        words = message.lower().split()
        if len(words) > 5:
            unique_words = set(words)
            if len(unique_words) / len(words) < 0.3:  # Less than 30% unique words
                raise ValidationError('Message appears to contain excessive repetition.')
        
        # Check for spam patterns
        spam_indicators = [
            'click here',
            'call now',
            'act now',
            'limited time',
            'free money',
            'guaranteed',
            'no obligation',
            'earn money fast',
            'work from home',
            'make money online',
        ]
        
        message_lower = message.lower()
        spam_count = sum(1 for indicator in spam_indicators if indicator in message_lower)
        if spam_count >= 2:
            raise ValidationError('Message contains content that appears to be spam.')
        
        # Check for excessive capitalization
        if len(re.findall(r'[A-Z]', message)) / len(message) > 0.5:
            raise ValidationError('Please avoid excessive capitalization.')
        
        # Remove HTML tags
        message = strip_tags(message)
        
        return message

    def clean(self):
        """Global form validation."""
        cleaned_data = super().clean()
        
        # Check for overall suspicious content
        name = cleaned_data.get('name', '')
        email = cleaned_data.get('email', '')
        subject = cleaned_data.get('subject', '')
        message = cleaned_data.get('message', '')
        
        # Honeypot check (if name and email are exactly the same)
        if name and email and name.lower() == email.split('@')[0].lower():
            raise ValidationError('Please fill out the form correctly.')
        
        # Check if all fields contain similar content (possible spam)
        if name and subject and message:
            fields_content = [name.lower(), subject.lower(), message.lower()]
            # If any two fields are too similar, it might be spam
            for i, content1 in enumerate(fields_content):
                for j, content2 in enumerate(fields_content[i+1:], i+1):
                    if len(content1) > 10 and len(content2) > 10:
                        # Simple similarity check
                        common_chars = set(content1) & set(content2)
                        if len(common_chars) / max(len(set(content1)), len(set(content2))) > 0.8:
                            raise ValidationError('Form fields appear to contain duplicate content.')
        
        return cleaned_data
