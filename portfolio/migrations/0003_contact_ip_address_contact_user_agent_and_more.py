# Generated by Django 5.2.3 on 2025-06-30 15:24

import django.core.validators
import portfolio.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_project_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, help_text='IP address of the sender (for security)', null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='user_agent',
            field=models.TextField(blank=True, help_text='Browser/device information (for security)', max_length=500),
        ),
        migrations.AlterField(
            model_name='contact',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='When the message was received'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(help_text="Contact's email address", max_length=254),
        ),
        migrations.AlterField(
            model_name='contact',
            name='is_read',
            field=models.BooleanField(default=False, help_text="Mark as read when you've reviewed the message"),
        ),
        migrations.AlterField(
            model_name='contact',
            name='message',
            field=models.TextField(help_text='Contact message content', max_length=2000),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(help_text="Contact's full name", max_length=100, validators=[django.core.validators.RegexValidator(message='Name can only contain letters, spaces, apostrophes, periods, and hyphens.', regex="^[a-zA-Z\\s\\'.-]+$")]),
        ),
        migrations.AlterField(
            model_name='contact',
            name='subject',
            field=models.CharField(help_text='Subject of the message', max_length=200),
        ),
        migrations.AlterField(
            model_name='education',
            name='degree',
            field=models.CharField(help_text='Degree or certification name', max_length=200),
        ),
        migrations.AlterField(
            model_name='education',
            name='description',
            field=models.TextField(blank=True, help_text='Additional details about your education', max_length=1000),
        ),
        migrations.AlterField(
            model_name='education',
            name='end_date',
            field=models.DateField(blank=True, help_text='When you completed this program (leave blank if ongoing)', null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='field_of_study',
            field=models.CharField(blank=True, help_text='Major, field of study, or specialization', max_length=200),
        ),
        migrations.AlterField(
            model_name='education',
            name='grade',
            field=models.CharField(blank=True, help_text='GPA, grade, or honors received', max_length=50),
        ),
        migrations.AlterField(
            model_name='education',
            name='institution',
            field=models.CharField(help_text='Educational institution name', max_length=200),
        ),
        migrations.AlterField(
            model_name='education',
            name='is_current',
            field=models.BooleanField(default=False, help_text="Check if you're currently enrolled"),
        ),
        migrations.AlterField(
            model_name='education',
            name='start_date',
            field=models.DateField(help_text='When you started this program'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='company',
            field=models.CharField(help_text='Company or organization name', max_length=200),
        ),
        migrations.AlterField(
            model_name='experience',
            name='company_url',
            field=models.URLField(blank=True, help_text='Company website URL', validators=[portfolio.models.validate_url_security]),
        ),
        migrations.AlterField(
            model_name='experience',
            name='description',
            field=models.TextField(help_text='Description of your role and achievements', max_length=2000),
        ),
        migrations.AlterField(
            model_name='experience',
            name='end_date',
            field=models.DateField(blank=True, help_text='When you ended this position (leave blank if current)', null=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='is_current',
            field=models.BooleanField(default=False, help_text='Check if this is your current position'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='location',
            field=models.CharField(blank=True, help_text='Work location (city, country or remote)', max_length=100),
        ),
        migrations.AlterField(
            model_name='experience',
            name='position',
            field=models.CharField(help_text='Your job title or position', max_length=200),
        ),
        migrations.AlterField(
            model_name='experience',
            name='start_date',
            field=models.DateField(help_text='When you started this position'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(help_text='Tell visitors about yourself (max 2000 characters)', max_length=2000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(help_text='Your contact email address', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='github',
            field=models.URLField(blank=True, help_text='Your GitHub profile URL', validators=[portfolio.models.validate_url_security]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='linkedin',
            field=models.URLField(blank=True, help_text='Your LinkedIn profile URL', validators=[portfolio.models.validate_url_security]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, help_text='Your location (city, country)', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(help_text='Your full name', max_length=100, validators=[django.core.validators.RegexValidator(message='Name can only contain letters, spaces, apostrophes, periods, and hyphens.', regex="^[a-zA-Z\\s\\'.-]+$")]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, help_text='Your phone number (10-15 digits)', max_length=20, validators=[portfolio.models.validate_phone_number]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, help_text='Profile photo (max 5MB, JPG/PNG/GIF/WebP)', null=True, upload_to='profile/', validators=[portfolio.models.validate_image_file]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='resume',
            field=models.FileField(blank=True, help_text='Your resume (max 5MB, PDF/DOC/DOCX)', null=True, upload_to='documents/', validators=[portfolio.models.validate_document_file]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='title',
            field=models.CharField(help_text='Your professional title or role', max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='twitter',
            field=models.URLField(blank=True, help_text='Your Twitter profile URL', validators=[portfolio.models.validate_url_security]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='website',
            field=models.URLField(blank=True, help_text='Your personal website URL', validators=[portfolio.models.validate_url_security]),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_date',
            field=models.DateField(help_text='Project completion or creation date'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(help_text='Detailed project description', max_length=5000),
        ),
        migrations.AlterField(
            model_name='project',
            name='github_url',
            field=models.URLField(blank=True, help_text='GitHub repository URL', validators=[portfolio.models.validate_url_security]),
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(blank=True, help_text='Project screenshot or image (max 5MB)', null=True, upload_to='projects/', validators=[portfolio.models.validate_image_file]),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_featured',
            field=models.BooleanField(default=False, help_text='Show this project in featured section'),
        ),
        migrations.AlterField(
            model_name='project',
            name='live_url',
            field=models.URLField(blank=True, help_text='Live demo URL', validators=[portfolio.models.validate_url_security]),
        ),
        migrations.AlterField(
            model_name='project',
            name='order',
            field=models.IntegerField(default=0, help_text='Display order (lower numbers appear first)'),
        ),
        migrations.AlterField(
            model_name='project',
            name='short_description',
            field=models.CharField(help_text='Brief description for project cards', max_length=300),
        ),
        migrations.AlterField(
            model_name='project',
            name='technologies',
            field=models.CharField(help_text='Comma-separated list of technologies used', max_length=500),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(help_text='Project title', max_length=200),
        ),
        migrations.AlterField(
            model_name='skill',
            name='icon',
            field=models.CharField(blank=True, help_text='CSS class for icon (e.g., fab fa-python)', max_length=100, validators=[django.core.validators.RegexValidator(message='Icon class can only contain letters, numbers, spaces, and hyphens.', regex='^[a-zA-Z0-9\\s-]+$')]),
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(help_text='Name of the skill or technology', max_length=100, validators=[django.core.validators.RegexValidator(message='Skill name can only contain letters, numbers, spaces, +, #, periods, and hyphens.', regex='^[a-zA-Z0-9\\s+#.-]+$')]),
        ),
        migrations.AlterField(
            model_name='skill',
            name='proficiency',
            field=models.IntegerField(default=80, help_text='Proficiency level (0-100%)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='skill',
            name='type',
            field=models.CharField(choices=[('technical', 'Technical'), ('soft', 'Soft Skills'), ('tools', 'Tools & Technologies')], default='technical', help_text='Category of the skill', max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='skill',
            unique_together={('name', 'type')},
        ),
        migrations.AddIndex(
            model_name='contact',
            index=models.Index(fields=['created_at'], name='portfolio_c_created_b56744_idx'),
        ),
        migrations.AddIndex(
            model_name='contact',
            index=models.Index(fields=['is_read'], name='portfolio_c_is_read_ddda81_idx'),
        ),
        migrations.AddIndex(
            model_name='contact',
            index=models.Index(fields=['email'], name='portfolio_c_email_09f1f3_idx'),
        ),
    ]
