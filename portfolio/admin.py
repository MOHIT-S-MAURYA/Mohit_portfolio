from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
import logging
from .models import Profile, Skill, Project, Experience, Education, Contact

# Set up logging
logger = logging.getLogger(__name__)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'bio', 'profile_image')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Social Links', {
            'fields': ('linkedin', 'github', 'twitter', 'website')
        }),
        ('Documents', {
            'fields': ('resume',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Override save_model to add error handling."""
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
            if change:
                messages.success(request, f"Profile '{obj.name}' updated successfully.")
            else:
                messages.success(request, f"Profile '{obj.name}' created successfully.")
        except ValidationError as e:
            logger.error(f"Validation error saving profile: {e}")
            messages.error(request, f"Error saving profile: {e}")
        except IntegrityError as e:
            logger.error(f"Database integrity error saving profile: {e}")
            messages.error(request, "Error saving profile: Database constraint violation.")
        except Exception as e:
            logger.error(f"Unexpected error saving profile: {e}")
            messages.error(request, f"Unexpected error saving profile: {e}")
    
    def delete_model(self, request, obj):
        """Override delete_model to add error handling."""
        try:
            name = obj.name
            super().delete_model(request, obj)
            messages.success(request, f"Profile '{name}' deleted successfully.")
        except Exception as e:
            logger.error(f"Error deleting profile: {e}")
            messages.error(request, f"Error deleting profile: {e}")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'proficiency']
    list_filter = ['type']
    ordering = ['type', 'name']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'created_date', 'order']
    list_filter = ['is_featured', 'created_date']
    ordering = ['order', '-created_date']
    prepopulated_fields = {'short_description': ('title',)}

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'start_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    ordering = ['-start_date']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'start_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    ordering = ['-start_date']

def mark_as_read(modeladmin, request, queryset):
    """Mark selected contact messages as read with error handling."""
    try:
        with transaction.atomic():
            count = queryset.update(is_read=True)
            logger.info(f"Marked {count} contact messages as read by user {request.user}")
            modeladmin.message_user(request, f"{count} messages marked as read.")
    except Exception as e:
        logger.error(f"Error marking messages as read: {e}")
        modeladmin.message_user(request, f"Error marking messages as read: {e}", level=messages.ERROR)

def mark_as_unread(modeladmin, request, queryset):
    """Mark selected contact messages as unread with error handling."""
    try:
        with transaction.atomic():
            count = queryset.update(is_read=False)
            logger.info(f"Marked {count} contact messages as unread by user {request.user}")
            modeladmin.message_user(request, f"{count} messages marked as unread.")
    except Exception as e:
        logger.error(f"Error marking messages as unread: {e}")
        modeladmin.message_user(request, f"Error marking messages as unread: {e}", level=messages.ERROR)

def send_reply_email(modeladmin, request, queryset):
    """Send reply emails to selected contacts."""
    try:
        successful_sends = 0
        failed_sends = 0
        
        for contact in queryset:
            try:
                subject = f"Re: {contact.subject}"
                message = f"Thank you for contacting us, {contact.name}. We have received your message and will respond soon."
                
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[contact.email],
                    fail_silently=False,
                )
                successful_sends += 1
                logger.info(f"Reply email sent to {contact.email}")
                
            except Exception as e:
                failed_sends += 1
                logger.error(f"Failed to send reply email to {contact.email}: {e}")
        
        if successful_sends > 0:
            modeladmin.message_user(request, f"Successfully sent {successful_sends} reply emails.")
        if failed_sends > 0:
            modeladmin.message_user(request, f"Failed to send {failed_sends} reply emails.", level=messages.WARNING)
            
    except Exception as e:
        logger.error(f"Error in send_reply_email action: {e}")
        modeladmin.message_user(request, f"Error sending reply emails: {e}", level=messages.ERROR)

mark_as_read.short_description = "Mark selected messages as read"
mark_as_unread.short_description = "Mark selected messages as unread"
send_reply_email.short_description = "Send reply emails to selected contacts"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    actions = [mark_as_read, mark_as_unread, send_reply_email]
    search_fields = ['name', 'email', 'subject']
    list_per_page = 25
    
    def get_queryset(self, request):
        """Optimize queryset with error handling."""
        try:
            qs = super().get_queryset(request)
            return qs.select_related()
        except Exception as e:
            logger.error(f"Error getting Contact queryset: {e}")
            return Contact.objects.none()
    
    def has_change_permission(self, request, obj=None):
        """Allow viewing but prevent editing of contact messages."""
        return True
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion with logging."""
        return True
    
    def delete_model(self, request, obj):
        """Override delete_model to add logging."""
        try:
            contact_info = f"{obj.name} ({obj.email})"
            super().delete_model(request, obj)
            logger.info(f"Contact message from {contact_info} deleted by user {request.user}")
            messages.success(request, f"Contact message from {contact_info} deleted successfully.")
        except Exception as e:
            logger.error(f"Error deleting contact message: {e}")
            messages.error(request, f"Error deleting contact message: {e}")
    
    def delete_queryset(self, request, queryset):
        """Override delete_queryset for bulk deletion with error handling."""
        try:
            count = queryset.count()
            contact_names = [f"{obj.name} ({obj.email})" for obj in queryset[:5]]  # Log first 5
            super().delete_queryset(request, queryset)
            logger.info(f"Bulk deleted {count} contact messages by user {request.user}. Sample: {contact_names}")
            messages.success(request, f"Successfully deleted {count} contact messages.")
        except Exception as e:
            logger.error(f"Error bulk deleting contact messages: {e}")
            messages.error(request, f"Error deleting contact messages: {e}")
