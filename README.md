# Personal Portfolio Website

A modern, responsive personal portfolio website built with Django. This project showcases a clean, professional design with sections for about, skills, projects, and contact information.

## Features

- **Modern Design**: Clean, professional UI with responsive design
- **Portfolio Sections**: Hero, About, Skills, Projects, Contact
- **Admin Panel**: Django admin for easy content management
- **Responsive**: Mobile-first design that looks great on all devices
- **SEO Friendly**: Optimized for search engines
- **Contact Form**: Working contact form with Django backend
- **Project Showcase**: Detailed project pages with galleries

## Tech Stack

- **Backend**: Django 5.2.3
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development)
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd portfolio-website
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Visit the site**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Email Configuration

To receive contact form messages via email, you need to configure email settings:

### Option 1: Using Management Command (Recommended)

```bash
# For Gmail
python manage.py setup_email --email your-email@gmail.com --password your-app-password --provider gmail

# For Outlook
python manage.py setup_email --email your-email@outlook.com --password your-password --provider outlook
```

### Option 2: Manual Configuration

1. **Copy the example file**
   ```bash
   cp local_settings_example.py portfolio_site/local_settings.py
   ```

2. **Edit the file with your email details**
   ```python
   # For Gmail (recommended)
   EMAIL_HOST_USER = 'your-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password, not regular password
   DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
   CONTACT_EMAIL = 'your-email@gmail.com'
   ```

### Gmail Setup Instructions

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password**:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and generate password
   - Use this generated password, not your regular Gmail password

### Test Email Configuration

```bash
python manage.py test_email --to your-email@gmail.com
```

### Development Mode

For development/testing without actual email sending:
```python
# In local_settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

This will print emails to the console instead of sending them.

## Project Structure

```
portfolio_site/
├── portfolio/                 # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── admin.py              # Admin configuration
│   ├── urls.py               # URL patterns
│   └── migrations/           # Database migrations
├── templates/                # HTML templates
│   ├── base.html            # Base template
│   └── portfolio/           # Portfolio templates
├── static/                  # Static files
│   ├── css/                 # Stylesheets
│   └── js/                  # JavaScript files
├── media/                   # User uploaded files
├── portfolio_site/          # Django project settings
└── manage.py               # Django management script
```

## Configuration

### Adding Content

1. **Profile Information**
   - Go to admin panel: `/admin/`
   - Add your profile information in the Profile section
   - Upload profile image and resume

2. **Skills**
   - Add your skills with proficiency levels
   - Categorize skills (Technical, Soft Skills, Tools)
   - Add Font Awesome icons for visual appeal

3. **Projects**
   - Add your projects with descriptions
   - Upload project images
   - Add technology stacks
   - Mark featured projects

4. **Experience & Education**
   - Add work experience and education details
   - Include dates, descriptions, and company URLs

### Customization

1. **Colors & Styling**
   - Edit `static/css/style.css` to customize colors and styling
   - Update CSS variables in `:root` section for easy theme changes

2. **Content**
   - Modify templates in `templates/portfolio/` for content changes
   - Update meta information in templates for SEO

3. **Features**
   - Add new models in `portfolio/models.py`
   - Create corresponding admin configurations
   - Update views and templates as needed

## Models

- **Profile**: Personal information, contact details, social links
- **Skill**: Technical and soft skills with proficiency levels
- **Project**: Portfolio projects with images, descriptions, links
- **Experience**: Work experience with dates and descriptions
- **Education**: Educational background
- **Contact**: Contact form submissions

## Admin Features

- User-friendly admin interface for all content
- Image upload for projects and profile
- Rich text editing for descriptions
- Bulk actions for managing multiple items
- Search and filtering capabilities

## Deployment

For production deployment:

1. **Security Settings**
   - Change `SECRET_KEY` in settings.py
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS`

2. **Static Files**
   - Configure static files collection
   - Set up media files serving

3. **Database**
   - Configure production database (PostgreSQL recommended)
   - Run migrations on production

4. **Web Server**
   - Configure with nginx/Apache and gunicorn
   - Set up SSL certificate

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you have any questions or need help with setup, please feel free to reach out or open an issue.
# Mohit_portfolio
