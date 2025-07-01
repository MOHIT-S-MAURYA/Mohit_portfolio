/* ===== CONTACT PAGE JAVASCRIPT ===== */

document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const contactForm = document.getElementById('contactForm');
    const submitButton = document.querySelector('.btn-primary[type="submit"]');
    const messageTextarea = document.getElementById('message');
    const messageCounter = document.getElementById('message-counter');
    const termsCheckbox = document.getElementById('terms');
    
    // Form validation
    function initFormValidation() {
        if (!contactForm) return;
        
        const formFields = contactForm.querySelectorAll('input, textarea, select');
        
        formFields.forEach(field => {
            // Real-time validation
            field.addEventListener('blur', function() {
                validateField(this);
            });
            
            field.addEventListener('input', function() {
                clearFieldError(this);
                
                // Special handling for message counter
                if (this.id === 'message') {
                    updateMessageCounter();
                }
            });
        });
    }
    
    // Validate individual field
    function validateField(field) {
        const value = field.value.trim();
        const fieldName = field.name || field.id;
        const fieldContainer = field.closest('.mb-3') || field.parentElement;
        
        // Remove existing validation
        clearFieldError(field);
        
        // Validation rules
        let isValid = true;
        let errorMessage = '';
        
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = `${getFieldLabel(field)} is required.`;
        } else if (field.type === 'email' && value && !isValidEmail(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address.';
        } else if (field.name === 'phone' && value && !isValidPhone(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid phone number.';
        } else if (field.id === 'message' && value.length < 10) {
            isValid = false;
            errorMessage = 'Message must be at least 10 characters long.';
        }
        
        // Display validation result
        if (isValid) {
            field.classList.add('is-valid');
            field.classList.remove('is-invalid');
        } else {
            field.classList.add('is-invalid');
            field.classList.remove('is-valid');
            showFieldError(field, errorMessage);
        }
        
        return isValid;
    }
    
    // Clear field error
    function clearFieldError(field) {
        field.classList.remove('is-valid', 'is-invalid');
        const errorElement = field.parentElement.querySelector('.field-validation-message');
        if (errorElement) {
            errorElement.remove();
        }
    }
    
    // Show field error
    function showFieldError(field, message) {
        const errorElement = document.createElement('div');
        errorElement.className = 'field-validation-message error';
        errorElement.textContent = message;
        field.parentElement.appendChild(errorElement);
    }
    
    // Get field label
    function getFieldLabel(field) {
        const label = document.querySelector(`label[for="${field.id}"]`);
        return label ? label.textContent.replace('*', '').trim() : field.name || field.id;
    }
    
    // Email validation
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    // Phone validation
    function isValidPhone(phone) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
    }
    
    // Message counter
    function updateMessageCounter() {
        if (!messageTextarea || !messageCounter) return;
        
        const currentLength = messageTextarea.value.length;
        const maxLength = messageTextarea.getAttribute('maxlength') || 1000;
        
        messageCounter.textContent = `${currentLength}/${maxLength}`;
        
        // Update counter color based on remaining characters
        messageCounter.classList.remove('warning', 'danger');
        
        const percentage = (currentLength / maxLength) * 100;
        if (percentage >= 90) {
            messageCounter.classList.add('danger');
        } else if (percentage >= 75) {
            messageCounter.classList.add('warning');
        }
    }
    
    // Form submission
    function initFormSubmission() {
        if (!contactForm) return;
        
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validate all fields
            const formFields = this.querySelectorAll('input, textarea, select');
            let isFormValid = true;
            
            formFields.forEach(field => {
                if (!validateField(field)) {
                    isFormValid = false;
                }
            });
            
            // Check terms checkbox
            if (termsCheckbox && !termsCheckbox.checked) {
                isFormValid = false;
                showGlobalError('Please accept the terms and conditions.');
            }
            
            if (isFormValid) {
                submitForm();
            } else {
                showGlobalError('Please correct the errors above and try again.');
            }
        });
    }
    
    // Submit form
    async function submitForm() {
        if (!submitButton) return;
        
        // Show loading state
        submitButton.classList.add('btn-loading');
        submitButton.disabled = true;
        
        try {
            const formData = new FormData(contactForm);
            
            // Simulate API call (replace with actual endpoint)
            const response = await fetch(contactForm.action || '/contact/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCsrfToken()
                }
            });
            
            if (response.ok) {
                showSuccessMessage();
                contactForm.reset();
                updateMessageCounter();
                
                // Track successful submission
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'form_submit', {
                        'event_category': 'engagement',
                        'event_label': 'Contact Form'
                    });
                }
            } else {
                throw new Error('Submission failed');
            }
        } catch (error) {
            console.error('Form submission error:', error);
            showGlobalError('An error occurred. Please try again later.');
        } finally {
            // Remove loading state
            submitButton.classList.remove('btn-loading');
            submitButton.disabled = false;
        }
    }
    
    // Get CSRF token
    function getCsrfToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : '';
    }
    
    // Show success message
    function showSuccessMessage() {
        const successDiv = document.createElement('div');
        successDiv.className = 'form-success';
        successDiv.innerHTML = `
            <i class="fas fa-check-circle me-2"></i>
            Thank you! Your message has been sent successfully. I'll get back to you soon.
        `;
        
        contactForm.insertAdjacentElement('afterend', successDiv);
        
        setTimeout(() => {
            successDiv.remove();
        }, 5000);
        
        // Scroll to success message
        successDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    // Show global error
    function showGlobalError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger';
        errorDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
        `;
        
        contactForm.insertAdjacentElement('beforebegin', errorDiv);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
    
    // Contact item click handlers
    function initContactItemEffects() {
        const contactItems = document.querySelectorAll('.contact-item');
        
        contactItems.forEach(item => {
            const link = item.querySelector('a');
            if (link) {
                item.addEventListener('click', function() {
                    link.click();
                    
                    // Track contact method usage
                    const contactType = this.querySelector('.contact-icon i').className;
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'contact_method_click', {
                            'event_category': 'engagement',
                            'event_label': contactType
                        });
                    }
                });
            }
        });
    }
    
    // Social link tracking
    function initSocialLinkTracking() {
        const socialLinks = document.querySelectorAll('.social-link');
        
        socialLinks.forEach(link => {
            link.addEventListener('click', function() {
                const platform = this.getAttribute('aria-label') || 'Unknown';
                
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'social_click', {
                        'event_category': 'engagement',
                        'event_label': platform
                    });
                }
            });
        });
    }
    
    // FAQ accordion enhancements
    function initFAQEnhancements() {
        const accordionButtons = document.querySelectorAll('.accordion-button');
        
        accordionButtons.forEach(button => {
            button.addEventListener('click', function() {
                const faqItem = this.closest('.accordion-item');
                const faqTitle = this.textContent.trim();
                
                // Track FAQ interactions
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'faq_click', {
                        'event_category': 'engagement',
                        'event_label': faqTitle
                    });
                }
            });
        });
    }
    
    // Terms modal handling
    function initTermsModal() {
        const termsLink = document.querySelector('[data-bs-target="#termsModal"]');
        if (termsLink) {
            termsLink.addEventListener('click', function() {
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'terms_view', {
                        'event_category': 'engagement',
                        'event_label': 'Terms Modal Open'
                    });
                }
            });
        }
    }
    
    // Floating help button
    function initFloatingHelp() {
        const helpButton = document.querySelector('.floating-help');
        if (helpButton) {
            helpButton.addEventListener('click', function() {
                const faqSection = document.getElementById('faq');
                if (faqSection) {
                    faqSection.scrollIntoView({ behavior: 'smooth' });
                }
                
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'help_click', {
                        'event_category': 'engagement',
                        'event_label': 'Floating Help Button'
                    });
                }
            });
        }
    }
    
    // Auto-save form data to localStorage
    function initAutoSave() {
        const formFields = contactForm?.querySelectorAll('input, textarea, select');
        const STORAGE_KEY = 'contact_form_data';
        
        // Load saved data
        function loadSavedData() {
            const savedData = localStorage.getItem(STORAGE_KEY);
            if (savedData) {
                try {
                    const data = JSON.parse(savedData);
                    Object.keys(data).forEach(key => {
                        const field = document.getElementById(key) || document.querySelector(`[name="${key}"]`);
                        if (field && field.type !== 'password') {
                            field.value = data[key];
                            if (field.id === 'message') {
                                updateMessageCounter();
                            }
                        }
                    });
                } catch (e) {
                    console.warn('Error loading saved form data:', e);
                }
            }
        }
        
        // Save form data
        function saveFormData() {
            const data = {};
            formFields?.forEach(field => {
                if (field.type !== 'password' && field.value) {
                    data[field.id || field.name] = field.value;
                }
            });
            localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        }
        
        // Clear saved data
        function clearSavedData() {
            localStorage.removeItem(STORAGE_KEY);
        }
        
        // Add event listeners
        formFields?.forEach(field => {
            field.addEventListener('input', debounce(saveFormData, 500));
        });
        
        // Load data on page load
        loadSavedData();
        
        // Clear data on successful submission
        contactForm?.addEventListener('submit', function() {
            setTimeout(clearSavedData, 1000);
        });
    }
    
    // Initialize all functionality
    function init() {
        initFormValidation();
        initFormSubmission();
        initContactItemEffects();
        initSocialLinkTracking();
        initFAQEnhancements();
        initTermsModal();
        initFloatingHelp();
        initAutoSave();
        updateMessageCounter();
    }
    
    // Start initialization
    init();
    
    // Performance monitoring
    function trackPagePerformance() {
        if ('performance' in window) {
            window.addEventListener('load', function() {
                setTimeout(function() {
                    const perfData = window.performance.timing;
                    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
                    console.log('Contact page loaded in:', pageLoadTime + 'ms');
                }, 0);
            });
        }
    }
    
    trackPagePerformance();
});

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export utilities for external use
window.ContactPageUtils = {
    validateForm: function() {
        // Public method for form validation
    },
    clearForm: function() {
        const form = document.getElementById('contactForm');
        if (form) {
            form.reset();
            const messageCounter = document.getElementById('message-counter');
            if (messageCounter) {
                messageCounter.textContent = '0/1000';
                messageCounter.classList.remove('warning', 'danger');
            }
        }
    }
};
