// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Active navigation link highlighting
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const currentPath = window.location.pathname;
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath || 
            (currentPath === '/' && link.getAttribute('href').includes('home'))) {
            link.classList.add('active');
        }
    });

    // Skill progress animation on scroll
    const skillBars = document.querySelectorAll('.progress-bar');
    const animateSkills = () => {
        skillBars.forEach(bar => {
            const rect = bar.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
            }
        });
    };

    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Animate skill bars
                if (entry.target.classList.contains('skills-section')) {
                    setTimeout(animateSkills, 200);
                }
            }
        });
    }, observerOptions);

    // Observe sections for animation
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        observer.observe(section);
    });

    // Enhanced Contact form handling with real-time validation
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        const submitBtn = contactForm.querySelector('#submitBtn');
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoading = submitBtn.querySelector('.btn-loading');
        const messageCounter = document.getElementById('message-counter');
        const messageField = contactForm.querySelector('#id_message');
        const termsCheckbox = contactForm.querySelector('#terms');
        
        // Character counter for message field
        if (messageField && messageCounter) {
            const updateCounter = () => {
                const count = messageField.value.length;
                messageCounter.textContent = count;
                messageCounter.style.color = count > 2000 ? '#dc3545' : count > 1800 ? '#ffc107' : '#6c757d';
            };
            
            messageField.addEventListener('input', updateCounter);
            updateCounter(); // Initial count
        }
        
        // Real-time field validation
        const validationFields = ['name', 'email', 'subject', 'message'];
        validationFields.forEach(fieldName => {
            const field = contactForm.querySelector(`#id_${fieldName}`);
            const validationDiv = contactForm.querySelector(`[data-field="${fieldName}"]`);
            
            if (field && validationDiv) {
                let validationTimeout;
                
                field.addEventListener('input', function() {
                    clearTimeout(validationTimeout);
                    
                    // Clear previous validation
                    validationDiv.innerHTML = '';
                    field.classList.remove('is-valid', 'is-invalid');
                    
                    // Skip validation for empty fields (except on blur)
                    if (!this.value.trim()) return;
                    
                    // Debounce validation
                    validationTimeout = setTimeout(() => {
                        validateField(fieldName, this.value, field, validationDiv);
                    }, 500);
                });
                
                field.addEventListener('blur', function() {
                    if (this.value.trim()) {
                        validateField(fieldName, this.value, field, validationDiv);
                    }
                });
            }
        });
        
        // AJAX field validation function
        function validateField(fieldName, fieldValue, fieldElement, validationDiv) {
            fetch('/ajax/validate-field/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': contactForm.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `field_name=${fieldName}&field_value=${encodeURIComponent(fieldValue)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.valid) {
                    fieldElement.classList.remove('is-invalid');
                    fieldElement.classList.add('is-valid');
                    validationDiv.innerHTML = '<div class="text-success small"><i class="fas fa-check"></i> Looks good!</div>';
                } else {
                    fieldElement.classList.remove('is-valid');
                    fieldElement.classList.add('is-invalid');
                    validationDiv.innerHTML = data.errors.map(error => 
                        `<div class="text-danger small"><i class="fas fa-exclamation-triangle"></i> ${error}</div>`
                    ).join('');
                }
            })
            .catch(error => {
                console.warn('Validation request failed:', error);
            });
        }
        
        // Form submission handling
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Check honeypot
            const honeypot = contactForm.querySelector('input[name="website"]');
            if (honeypot && honeypot.value) {
                showFormMessage('error', 'Form submission failed. Please try again.');
                return;
            }
            
            // Check terms checkbox
            if (!termsCheckbox.checked) {
                showFormMessage('error', 'Please accept the terms and conditions to continue.');
                termsCheckbox.focus();
                return;
            }
            
            // Validate all fields before submission
            let isValid = true;
            const formData = new FormData(contactForm);
            
            validationFields.forEach(fieldName => {
                const field = contactForm.querySelector(`#id_${fieldName}`);
                if (field && !field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                }
            });
            
            if (!isValid) {
                showFormMessage('error', 'Please fill in all required fields.');
                return;
            }
            
            // Show loading state
            submitBtn.disabled = true;
            btnText.classList.add('d-none');
            btnLoading.classList.remove('d-none');
            
            // Submit the form
            fetch(contactForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': contactForm.querySelector('[name=csrfmiddlewaretoken]').value,
                }
            })
            .then(response => {
                if (response.ok) {
                    return response.text();
                }
                throw new Error('Network response was not ok');
            })
            .then(html => {
                // Parse response to check for success
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = html;
                const alerts = tempDiv.querySelectorAll('.alert');
                
                let hasSuccess = false;
                alerts.forEach(alert => {
                    if (alert.classList.contains('alert-success')) {
                        hasSuccess = true;
                        showFormMessage('success', alert.textContent.trim());
                        contactForm.reset();
                        // Reset all validation states
                        contactForm.querySelectorAll('.is-valid, .is-invalid').forEach(el => {
                            el.classList.remove('is-valid', 'is-invalid');
                        });
                        // Clear validation messages
                        contactForm.querySelectorAll('.field-validation-message').forEach(el => {
                            el.innerHTML = '';
                        });
                        // Reset counter
                        if (messageCounter) messageCounter.textContent = '0';
                        // Uncheck terms
                        if (termsCheckbox) termsCheckbox.checked = false;
                    } else if (alert.classList.contains('alert-danger')) {
                        showFormMessage('error', alert.textContent.trim());
                    }
                });
                
                if (!hasSuccess && alerts.length === 0) {
                    // Check if form was redirected (success case)
                    showFormMessage('success', '🎉 Thank you for your message! I will get back to you soon.');
                    contactForm.reset();
                }
            })
            .catch(error => {
                console.error('Form submission error:', error);
                showFormMessage('error', 'An error occurred. Please try again or email me directly.');
            })
            .finally(() => {
                // Reset button state
                submitBtn.disabled = false;
                btnText.classList.remove('d-none');
                btnLoading.classList.add('d-none');
            });
        });
        
        // Show form messages
        function showFormMessage(type, message) {
            const messagesDiv = document.getElementById('form-messages');
            const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
            const icon = type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-triangle';
            
            messagesDiv.innerHTML = `
                <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                    <i class="${icon} me-2"></i>${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
            
            // Scroll to message
            messagesDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            
            // Auto-hide success messages after 5 seconds
            if (type === 'success') {
                setTimeout(() => {
                    const alert = messagesDiv.querySelector('.alert');
                    if (alert) {
                        alert.classList.remove('show');
                        setTimeout(() => messagesDiv.innerHTML = '', 300);
                    }
                }, 5000);
            }
        }
        
        // Prevent multiple submissions
        let isSubmitting = false;
        contactForm.addEventListener('submit', function(e) {
            if (isSubmitting) {
                e.preventDefault();
                return false;
            }
            isSubmitting = true;
            
            // Reset flag after 3 seconds
            setTimeout(() => {
                isSubmitting = false;
            }, 3000);
        });
    }

    // Navbar background on scroll
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Project image lazy loading
    const projectImages = document.querySelectorAll('.project-image img');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            }
        });
    });

    projectImages.forEach(img => {
        imageObserver.observe(img);
    });

    // Typing animation for hero title
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const text = heroTitle.textContent;
        heroTitle.textContent = '';
        let i = 0;
        
        const typeWriter = () => {
            if (i < text.length) {
                heroTitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };
        
        setTimeout(typeWriter, 1000);
    }
});

// Utility functions
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Add CSS classes for animations
const style = document.createElement('style');
style.textContent = `
    .animate-in {
        animation: fadeInUp 0.8s ease forwards;
    }
    
    .navbar.scrolled {
        background-color: rgba(52, 58, 64, 0.98) !important;
        backdrop-filter: blur(20px);
    }
    
    .project-image img {
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .project-image img.loaded {
        opacity: 1;
    }
`;
document.head.appendChild(style);
