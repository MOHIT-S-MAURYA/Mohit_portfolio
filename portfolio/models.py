from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.html import strip_tags
from django.utils import timezone
import re

def validate_file_size(file):
    """Validate uploaded file size (max 5MB)."""
    if file:
        filesize = file.size
        if filesize > 5 * 1024 * 1024:  # 5MB
            raise ValidationError("File size cannot exceed 5MB.")

def validate_image_file(file):
    """Validate uploaded image files."""
    if file:
        validate_file_size(file)
        # Check file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        if not any(file.name.lower().endswith(ext) for ext in valid_extensions):
            raise ValidationError("Only image files (JPG, PNG, GIF, WebP) are allowed.")

def validate_document_file(file):
    """Validate uploaded document files."""
    if file:
        validate_file_size(file)
        # Check file extension
        valid_extensions = ['.pdf', '.doc', '.docx']
        if not any(file.name.lower().endswith(ext) for ext in valid_extensions):
            raise ValidationError("Only PDF and Word documents are allowed.")

def validate_phone_number(phone):
    """Validate phone number format."""
    if phone:
        # Remove all non-digit characters for validation
        digits_only = re.sub(r'\D', '', phone)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValidationError("Phone number must be between 10 and 15 digits.")

def validate_url_security(url):
    """Validate URL for security."""
    if url:
        # Check for suspicious protocols
        if not url.startswith(('http://', 'https://')):
            raise ValidationError("URL must start with http:// or https://")
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'javascript:',
            r'data:',
            r'vbscript:',
            r'file:',
            r'ftp:',
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                raise ValidationError("URL contains potentially unsafe content.")

class Profile(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s\'.-]+$',
                message='Name can only contain letters, spaces, apostrophes, periods, and hyphens.'
            )
        ],
        help_text="Your full name"
    )
    title = models.CharField(
        max_length=200,
        help_text="Your professional title or role"
    )
    bio = models.TextField(
        max_length=2000,
        help_text="Tell visitors about yourself (max 2000 characters)"
    )
    profile_image = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True,
        validators=[validate_image_file],
        help_text="Profile photo (max 5MB, JPG/PNG/GIF/WebP)"
    )
    resume = models.FileField(
        upload_to='documents/',
        blank=True,
        null=True,
        validators=[validate_document_file],
        help_text="Your resume (max 5MB, PDF/DOC/DOCX)"
    )
    email = models.EmailField(
        unique=True,
        help_text="Your contact email address"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[validate_phone_number],
        help_text="Your phone number (10-15 digits)"
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        help_text="Your location (city, country)"
    )
    linkedin = models.URLField(
        blank=True,
        validators=[validate_url_security],
        help_text="Your LinkedIn profile URL"
    )
    github = models.URLField(
        blank=True,
        validators=[validate_url_security],
        help_text="Your GitHub profile URL"
    )
    twitter = models.URLField(
        blank=True,
        validators=[validate_url_security],
        help_text="Your Twitter profile URL"
    )
    website = models.URLField(
        blank=True,
        validators=[validate_url_security],
        help_text="Your personal website URL"
    )
    
    def clean(self):
        """Custom model validation."""
        super().clean()
        
        # Validate name
        if self.name:
            self.name = self.name.strip()
            if len(self.name) < 2:
                raise ValidationError({'name': 'Name must be at least 2 characters long.'})
        
        # Validate bio
        if self.bio:
            self.bio = strip_tags(self.bio.strip())
            if len(self.bio) < 10:
                raise ValidationError({'bio': 'Bio must be at least 10 characters long.'})
        
        # Validate email format more strictly
        if self.email:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.email):
                raise ValidationError({'email': 'Please enter a valid email address.'})
    
    def save(self, *args, **kwargs):
        """Override save to perform additional validation."""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

class Skill(models.Model):
    SKILL_TYPES = [
        ('technical', 'Technical'),
        ('soft', 'Soft Skills'),
        ('tools', 'Tools & Technologies'),
    ]
    
    name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\s+#.-]+$',
                message='Skill name can only contain letters, numbers, spaces, +, #, periods, and hyphens.'
            )
        ],
        help_text="Name of the skill or technology"
    )
    type = models.CharField(
        max_length=20,
        choices=SKILL_TYPES,
        default='technical',
        help_text="Category of the skill"
    )
    proficiency = models.IntegerField(
        default=80,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Proficiency level (0-100%)"
    )
    icon = models.CharField(
        max_length=100,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\s-]+$',
                message='Icon class can only contain letters, numbers, spaces, and hyphens.'
            )
        ],
        help_text="CSS class for icon (e.g., fab fa-python)"
    )
    
    def clean(self):
        """Custom model validation."""
        super().clean()
        
        if self.name:
            self.name = self.name.strip()
            if len(self.name) < 2:
                raise ValidationError({'name': 'Skill name must be at least 2 characters long.'})
        
        if self.proficiency < 0 or self.proficiency > 100:
            raise ValidationError({'proficiency': 'Proficiency must be between 0 and 100.'})
    
    def save(self, *args, **kwargs):
        """Override save to perform additional validation."""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.proficiency}%)"
    
    class Meta:
        ordering = ['type', 'name']
        unique_together = ['name', 'type']  # Prevent duplicate skills

class Project(models.Model):
    title = models.CharField(
        max_length=200,
        help_text="Project title"
    )
    description = models.TextField(
        max_length=5000,
        help_text="Detailed project description"
    )
    short_description = models.CharField(
        max_length=300,
        help_text="Brief description for project cards"
    )
    image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True,
        validators=[validate_image_file],
        help_text="Project screenshot or image (max 5MB)"
    )
    technologies = models.CharField(
        max_length=500,
        help_text="Comma-separated list of technologies used"
    )
    github_url = models.URLField(
        blank=True,
        validators=[validate_url_security],
        help_text="GitHub repository URL"
    )
    live_url = models.URLField(
        blank=True,
        validators=[validate_url_security],
        help_text="Live demo URL"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Show this project in featured section"
    )
    created_date = models.DateField(
        help_text="Project completion or creation date"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    
    def clean(self):
        """Custom model validation."""
        super().clean()
        
        if self.title:
            self.title = strip_tags(self.title.strip())
            if len(self.title) < 3:
                raise ValidationError({'title': 'Project title must be at least 3 characters long.'})
        
        if self.description:
            self.description = strip_tags(self.description.strip())
            if len(self.description) < 10:
                raise ValidationError({'description': 'Project description must be at least 10 characters long.'})
        
        if self.short_description:
            self.short_description = strip_tags(self.short_description.strip())
            if len(self.short_description) < 10:
                raise ValidationError({'short_description': 'Short description must be at least 10 characters long.'})
        
        if self.technologies:
            # Validate technologies format
            tech_list = [tech.strip() for tech in self.technologies.split(',')]
            if len(tech_list) < 1:
                raise ValidationError({'technologies': 'At least one technology must be specified.'})
            
            # Check each technology
            for tech in tech_list:
                if not re.match(r'^[a-zA-Z0-9\s+#.-]+$', tech):
                    raise ValidationError({'technologies': f'Technology "{tech}" contains invalid characters.'})
    
    def save(self, *args, **kwargs):
        """Override save to perform additional validation."""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_technologies_list(self):
        """Return cleaned list of technologies."""
        if not self.technologies:
            return []
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]
    
    class Meta:
        ordering = ['order', '-created_date']

class Experience(models.Model):
    company = models.CharField(
        max_length=200,
        help_text="Company or organization name"
    )
    position = models.CharField(
        max_length=200,
        help_text="Your job title or position"
    )
    description = models.TextField(
        max_length=2000,
        help_text="Description of your role and achievements"
    )
    start_date = models.DateField(
        help_text="When you started this position"
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text="When you ended this position (leave blank if current)"
    )
    is_current = models.BooleanField(
        default=False,
        help_text="Check if this is your current position"
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        help_text="Work location (city, country or remote)"
    )
    company_url = models.URLField(
        blank=True,
        validators=[validate_url_security],
        help_text="Company website URL"
    )
    
    def clean(self):
        """Custom model validation."""
        super().clean()
        
        if self.company:
            self.company = strip_tags(self.company.strip())
            if len(self.company) < 2:
                raise ValidationError({'company': 'Company name must be at least 2 characters long.'})
        
        if self.position:
            self.position = strip_tags(self.position.strip())
            if len(self.position) < 2:
                raise ValidationError({'position': 'Position title must be at least 2 characters long.'})
        
        if self.description:
            self.description = strip_tags(self.description.strip())
            if len(self.description) < 10:
                raise ValidationError({'description': 'Description must be at least 10 characters long.'})
        
        # Validate date logic
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError({'end_date': 'End date must be after start date.'})
        
        if self.is_current and self.end_date:
            raise ValidationError({'end_date': 'End date should be empty for current positions.'})
    
    def save(self, *args, **kwargs):
        """Override save to perform additional validation."""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.position} at {self.company}"
    
    class Meta:
        ordering = ['-start_date']

class Education(models.Model):
    institution = models.CharField(
        max_length=200,
        help_text="Educational institution name"
    )
    degree = models.CharField(
        max_length=200,
        help_text="Degree or certification name"
    )
    field_of_study = models.CharField(
        max_length=200,
        blank=True,
        help_text="Major, field of study, or specialization"
    )
    start_date = models.DateField(
        help_text="When you started this program"
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text="When you completed this program (leave blank if ongoing)"
    )
    is_current = models.BooleanField(
        default=False,
        help_text="Check if you're currently enrolled"
    )
    grade = models.CharField(
        max_length=50,
        blank=True,
        help_text="GPA, grade, or honors received"
    )
    description = models.TextField(
        blank=True,
        max_length=1000,
        help_text="Additional details about your education"
    )
    
    def clean(self):
        """Custom model validation."""
        super().clean()
        
        if self.institution:
            self.institution = strip_tags(self.institution.strip())
            if len(self.institution) < 2:
                raise ValidationError({'institution': 'Institution name must be at least 2 characters long.'})
        
        if self.degree:
            self.degree = strip_tags(self.degree.strip())
            if len(self.degree) < 2:
                raise ValidationError({'degree': 'Degree name must be at least 2 characters long.'})
        
        if self.field_of_study:
            self.field_of_study = strip_tags(self.field_of_study.strip())
        
        if self.description:
            self.description = strip_tags(self.description.strip())
        
        # Validate start date is not in the future
        if self.start_date and self.start_date > timezone.now().date():
            raise ValidationError({'start_date': 'Start date cannot be in the future.'})
        
        # Validate end date is not in the future (unless it's current)
        if self.end_date and not self.is_current and self.end_date > timezone.now().date():
            raise ValidationError({'end_date': 'End date cannot be in the future.'})
        
        # Validate date logic
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError({'end_date': 'End date must be after start date.'})
        
        if self.is_current and self.end_date:
            raise ValidationError({'end_date': 'End date should be empty for current education.'})
    
    def save(self, *args, **kwargs):
        """Override save to perform additional validation."""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.degree} from {self.institution}"
    
    class Meta:
        ordering = ['-start_date']

class Contact(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s\'.-]+$',
                message='Name can only contain letters, spaces, apostrophes, periods, and hyphens.'
            )
        ],
        help_text="Contact's full name"
    )
    email = models.EmailField(
        help_text="Contact's email address"
    )
    subject = models.CharField(
        max_length=200,
        help_text="Subject of the message"
    )
    message = models.TextField(
        max_length=2000,
        help_text="Contact message content"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the message was received"
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Mark as read when you've reviewed the message"
    )
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text="IP address of the sender (for security)"
    )
    user_agent = models.TextField(
        blank=True,
        max_length=500,
        help_text="Browser/device information (for security)"
    )
    
    def clean(self):
        """Custom model validation."""
        super().clean()
        
        if self.name:
            self.name = self.name.strip()
            if len(self.name) < 2:
                raise ValidationError({'name': 'Name must be at least 2 characters long.'})
        
        if self.email:
            # Additional email validation
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.email):
                raise ValidationError({'email': 'Please enter a valid email address.'})
        
        if self.subject:
            self.subject = strip_tags(self.subject.strip())
            if len(self.subject) < 5:
                raise ValidationError({'subject': 'Subject must be at least 5 characters long.'})
        
        if self.message:
            self.message = strip_tags(self.message.strip())
            if len(self.message) < 10:
                raise ValidationError({'message': 'Message must be at least 10 characters long.'})
    
    def save(self, *args, **kwargs):
        """Override save to perform additional validation."""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['is_read']),
            models.Index(fields=['email']),
        ]
