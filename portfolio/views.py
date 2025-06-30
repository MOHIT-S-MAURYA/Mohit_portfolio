from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
import json
from .models import Profile, Skill, Project, Experience, Education, Contact
from .forms import ContactForm

# Set up logging
logger = logging.getLogger(__name__)

def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_profile_safe():
    """Safely get profile object with error handling."""
    try:
        profile = Profile.objects.first()
        if not profile:
            logger.warning("No profile found in database")
        return profile
    except Exception as e:
        logger.error(f"Error fetching profile: {e}")
        return None

@cache_page(60 * 15)  # Cache for 15 minutes
def home(request):
    """Home page view with comprehensive error handling."""
    context = {}
    
    try:
        # Get profile with error handling
        context['profile'] = get_profile_safe()
        
        # Get featured projects with error handling
        try:
            context['featured_projects'] = Project.objects.filter(is_featured=True).select_related()[:3]
        except Exception as e:
            logger.error(f"Error fetching featured projects: {e}")
            context['featured_projects'] = []
        
        # Get skills with error handling
        try:
            context['skills'] = Skill.objects.all()[:12]  # Limit to prevent page bloat
        except Exception as e:
            logger.error(f"Error fetching skills: {e}")
            context['skills'] = []
        
        # Get recent experience with error handling
        try:
            context['recent_experience'] = Experience.objects.all()[:3]
        except Exception as e:
            logger.error(f"Error fetching recent experience: {e}")
            context['recent_experience'] = []
            
    except Exception as e:
        logger.error(f"Unexpected error in home view: {e}")
        messages.error(request, "Some content may not be available right now. Please try again later.")
    
    return render(request, 'portfolio/home.html', context)

@cache_page(60 * 10)  # Cache for 10 minutes
def about(request):
    """About page view with comprehensive error handling."""
    context = {}
    
    try:
        # Get profile with error handling
        context['profile'] = get_profile_safe()
        
        # Get skills grouped by type
        try:
            context['skills'] = Skill.objects.all().order_by('type', 'name')
        except Exception as e:
            logger.error(f"Error fetching skills: {e}")
            context['skills'] = []
        
        # Get experience with error handling
        try:
            context['experience'] = Experience.objects.all()
        except Exception as e:
            logger.error(f"Error fetching experience: {e}")
            context['experience'] = []
        
        # Get education with error handling
        try:
            context['education'] = Education.objects.all()
        except Exception as e:
            logger.error(f"Error fetching education: {e}")
            context['education'] = []
            
    except Exception as e:
        logger.error(f"Unexpected error in about view: {e}")
        messages.error(request, "Some content may not be available right now. Please try again later.")
    
    return render(request, 'portfolio/about.html', context)

class ProjectListView(ListView):
    """Enhanced project list view with error handling and pagination."""
    model = Project
    template_name = 'portfolio/projects.html'
    context_object_name = 'projects'
    paginate_by = 6
    
    def get_queryset(self):
        """Get projects with error handling."""
        try:
            return Project.objects.all().order_by('order', '-created_date')
        except Exception as e:
            logger.error(f"Error fetching projects: {e}")
            return Project.objects.none()
    
    def get_context_data(self, **kwargs):
        """Add additional context with error handling."""
        context = super().get_context_data(**kwargs)
        
        try:
            context['profile'] = get_profile_safe()
            
            # Add featured projects count
            context['featured_count'] = Project.objects.filter(is_featured=True).count()
            
            # Add total projects count
            context['total_count'] = Project.objects.count()
            
        except Exception as e:
            logger.error(f"Error in ProjectListView context: {e}")
            context['featured_count'] = 0
            context['total_count'] = 0
        
        return context
    
    def dispatch(self, request, *args, **kwargs):
        """Handle view-level errors."""
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in ProjectListView dispatch: {e}")
            messages.error(request, "Unable to load projects. Please try again later.")
            return redirect('home')

class ProjectDetailView(DetailView):
    """Enhanced project detail view with error handling."""
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    
    def get_object(self, queryset=None):
        """Get project object with enhanced error handling."""
        try:
            obj = super().get_object(queryset)
            return obj
        except Http404:
            logger.warning(f"Project with pk={self.kwargs.get('pk')} not found")
            raise Http404("Project not found")
        except Exception as e:
            logger.error(f"Error fetching project: {e}")
            raise Http404("Unable to load project")
    
    def get_context_data(self, **kwargs):
        """Add additional context with error handling."""
        context = super().get_context_data(**kwargs)
        
        try:
            context['profile'] = get_profile_safe()
            
            # Get related projects (same technologies)
            project = self.get_object()
            if project and project.technologies:
                try:
                    # Get projects with similar technologies
                    tech_list = project.get_technologies_list()
                    if tech_list:
                        related_projects = Project.objects.exclude(
                            pk=project.pk
                        ).filter(
                            technologies__icontains=tech_list[0]
                        )[:3]
                        context['related_projects'] = related_projects
                except Exception as e:
                    logger.error(f"Error fetching related projects: {e}")
                    context['related_projects'] = []
            
        except Exception as e:
            logger.error(f"Error in ProjectDetailView context: {e}")
            context['related_projects'] = []
        
        return context
    
    def dispatch(self, request, *args, **kwargs):
        """Handle view-level errors."""
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            messages.error(request, "The requested project could not be found.")
            return redirect('projects')
        except Exception as e:
            logger.error(f"Error in ProjectDetailView dispatch: {e}")
            messages.error(request, "Unable to load project details. Please try again later.")
            return redirect('projects')

@csrf_protect
@require_http_methods(["GET", "POST"])
def contact(request):
    """Enhanced contact view with comprehensive validation and error handling."""
    
    # Rate limiting check (simple implementation)
    session_key = f"contact_attempts_{get_client_ip(request)}"
    attempts = request.session.get(session_key, 0)
    
    if attempts >= 5:  # Max 5 attempts per session
        messages.error(request, "⚠️ Too many contact attempts. Please try again later.")
        logger.warning(f"Rate limit exceeded for IP: {get_client_ip(request)}")
        return redirect('contact')
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        # Increment attempt counter
        request.session[session_key] = attempts + 1
        request.session.set_expiry(3600)  # 1 hour expiry
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create contact object with additional security info
                    contact_obj = form.save(commit=False)
                    contact_obj.ip_address = get_client_ip(request)
                    contact_obj.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
                    contact_obj.save()
                    
                    # Send emails
                    success = send_contact_emails(
                        contact_obj.name,
                        contact_obj.email,
                        contact_obj.subject,
                        contact_obj.message
                    )
                    
                    if success:
                        messages.success(
                            request,
                            '🎉 Thank you for your message! I will get back to you within 24-48 hours.'
                        )
                        # Reset attempt counter on success
                        request.session.pop(session_key, None)
                    else:
                        messages.success(
                            request,
                            '🎉 Thank you for your message! I will get back to you soon.'
                        )
                    
                    logger.info(f"Contact form submitted successfully by {contact_obj.email}")
                    return redirect('contact')
                    
            except ValidationError as e:
                logger.warning(f"Validation error in contact form: {e}")
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
                        
            except IntegrityError as e:
                logger.error(f"Database integrity error in contact form: {e}")
                messages.error(request, "⚠️ Unable to save your message. Please try again.")
                
            except Exception as e:
                logger.error(f"Unexpected error in contact form: {e}")
                messages.error(request, "⚠️ An unexpected error occurred. Please try again later.")
        
        else:
            # Form validation failed
            logger.warning(f"Contact form validation failed: {form.errors}")
            messages.error(request, "⚠️ Please correct the errors below and try again.")
    
    else:
        form = ContactForm()
    
    # Get profile for contact info
    try:
        profile = get_profile_safe()
    except Exception as e:
        logger.error(f"Error fetching profile for contact page: {e}")
        profile = None
    
    context = {
        'profile': profile,
        'form': form
    }
    
    return render(request, 'portfolio/contact.html', context)

def send_contact_emails(name, email, subject, message):
    """
    Send contact form emails with comprehensive error handling.
    Returns True if emails sent successfully, False otherwise.
    """
    try:
        current_time = timezone.now()
        
        # Email context for templates
        email_context = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'timestamp': current_time,
        }
        
        email_sent = False
        
        # Send admin notification email
        contact_email = getattr(settings, 'CONTACT_EMAIL', None)
        if contact_email and hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER:
            try:
                admin_subject = f'🔔 New Contact: {subject}'
                
                # Render HTML email template
                admin_html_content = render_to_string('emails/admin_notification.html', email_context)
                
                # Plain text fallback
                admin_text_content = f"""
New Contact Form Message Received

Name: {name}
Email: {email}
Subject: {subject}
Received: {current_time.strftime('%B %d, %Y at %I:%M %p')}

Message:
{message}

---
Reply to {email} to respond to this inquiry.
This email was automatically generated from your portfolio website.
"""
                
                # Create and send admin email
                admin_email = EmailMultiAlternatives(
                    admin_subject,
                    admin_text_content,
                    settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                    [contact_email],
                )
                admin_email.attach_alternative(admin_html_content, "text/html")
                admin_email.send(fail_silently=False)
                email_sent = True
                
                logger.info(f"Admin notification email sent for contact from {email}")
                
            except Exception as e:
                logger.error(f"Failed to send admin notification email: {e}")
        
        # Send user confirmation email
        try:
            user_subject = '✨ Thank you for contacting me - Mohit Maurya'
            
            # Render HTML confirmation email
            user_html_content = render_to_string('emails/user_confirmation.html', email_context)
            
            # Plain text fallback
            user_text_content = f"""
Hi {name},

Thank you for reaching out through my portfolio website! I really appreciate your interest and the time you took to send me a message.

Your Message Summary:
Subject: {subject}
Sent on: {current_time.strftime('%B %d, %Y at %I:%M %p')}

I've received your message and will get back to you within 24-48 hours.

For urgent inquiries, you can also reach me directly at: msm606248@gmail.com

Best regards,
Mohit Maurya
Full Stack Developer

---
This is an automated confirmation email.
Please do not reply to this email. For direct communication, use: msm606248@gmail.com
"""
            
            # Create and send user confirmation email
            user_email = EmailMultiAlternatives(
                user_subject,
                user_text_content,
                settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                [email],
            )
            user_email.attach_alternative(user_html_content, "text/html")
            user_email.send(fail_silently=True)  # Don't fail if confirmation email fails
            
            logger.info(f"User confirmation email sent to {email}")
            
        except Exception as e:
            logger.error(f"Failed to send user confirmation email: {e}")
            # Don't fail the whole process if user email fails
        
        return email_sent
        
    except Exception as e:
        logger.error(f"Unexpected error in send_contact_emails: {e}")
        return False

# AJAX view for form validation
@require_http_methods(["POST"])
def validate_contact_field(request):
    """AJAX endpoint for real-time form validation."""
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    try:
        field_name = request.POST.get('field_name')
        field_value = request.POST.get('field_value')
        
        if not field_name or field_value is None:
            return JsonResponse({'error': 'Missing parameters'}, status=400)
        
        form = ContactForm(data={field_name: field_value})
        form.is_valid()  # Trigger validation
        
        field_errors = form.errors.get(field_name, [])
        
        return JsonResponse({
            'valid': len(field_errors) == 0,
            'errors': field_errors
        })
        
    except Exception as e:
        logger.error(f"Error in validate_contact_field: {e}")
        return JsonResponse({'error': 'Validation failed'}, status=500)

# Custom error handlers
def custom_404(request, exception):
    """Custom 404 error handler."""
    logger.warning(f"404 error for URL: {request.path} from IP: {get_client_ip(request)}")
    return render(request, '404.html', status=404)

def custom_500(request):
    """Custom 500 error handler."""
    logger.error(f"500 error for URL: {request.path} from IP: {get_client_ip(request)}")
    return render(request, '500.html', status=500)

def custom_403(request, exception):
    """Custom 403 error handler."""
    logger.warning(f"403 error for URL: {request.path} from IP: {get_client_ip(request)}")
    return render(request, '403.html', status=403)

def terms(request):
    """Terms and conditions page view."""
    try:
        logger.info(f"Terms page accessed from IP: {get_client_ip(request)}")
        return render(request, 'portfolio/terms.html')
    except Exception as e:
        logger.error(f"Error rendering terms page: {e}")
        messages.error(request, "There was an error loading the terms page.")
        return redirect('portfolio:home')
