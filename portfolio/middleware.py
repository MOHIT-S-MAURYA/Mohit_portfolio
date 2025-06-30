import logging
import traceback
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.conf import settings

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware(MiddlewareMixin):
    """
    Custom middleware for enhanced error handling and logging.
    """

    def process_exception(self, request, exception):
        """
        Process exceptions and provide appropriate responses.
        """
        # Get client IP for logging
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Log the exception with context
        error_context = {
            'path': request.path,
            'method': request.method,
            'ip': ip,
            'user': request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous',
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'exception_type': type(exception).__name__,
            'exception_message': str(exception),
        }

        # Handle different types of exceptions
        if isinstance(exception, Http404):
            logger.warning(f"404 error: {error_context}")
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({
                    'error': 'Not found',
                    'message': 'The requested resource was not found.'
                }, status=404)
            return render(request, '404.html', status=404)

        elif isinstance(exception, PermissionDenied):
            logger.warning(f"403 error: {error_context}")
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({
                    'error': 'Forbidden',
                    'message': 'You do not have permission to access this resource.'
                }, status=403)
            return render(request, '403.html', status=403)

        elif isinstance(exception, ValidationError):
            logger.warning(f"Validation error: {error_context}")
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({
                    'error': 'Validation error',
                    'message': str(exception)
                }, status=400)

        else:
            # Log full traceback for unexpected errors
            error_context['traceback'] = traceback.format_exc()
            logger.error(f"Unexpected error: {error_context}")
            
            if not settings.DEBUG:
                if request.headers.get('Accept') == 'application/json':
                    return JsonResponse({
                        'error': 'Internal server error',
                        'message': 'An unexpected error occurred. Please try again later.'
                    }, status=500)
                return render(request, '500.html', status=500)

        # Let Django handle the exception normally if not handled above
        return None

    def process_response(self, request, response):
        """
        Process responses and log any errors.
        """
        # Log 4xx and 5xx responses
        if response.status_code >= 400:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            log_data = {
                'status_code': response.status_code,
                'path': request.path,
                'method': request.method,
                'ip': ip,
                'user': request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous',
            }

            if response.status_code >= 500:
                logger.error(f"5xx response: {log_data}")
            else:
                logger.warning(f"4xx response: {log_data}")

        return response
