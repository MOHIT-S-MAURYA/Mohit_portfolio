// Enhanced Dark Mode Management
class ThemeManager {
    constructor() {
        this.currentTheme = null;
        this.prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
        this.init();
    }

    init() {
        // Initialize theme from localStorage or system preference
        const savedTheme = localStorage.getItem('theme');
        const systemTheme = this.prefersDark.matches ? 'dark' : 'light';
        this.setTheme(savedTheme || systemTheme);

        // Listen for system theme changes
        this.prefersDark.addListener((e) => {
            if (!localStorage.getItem('theme')) {
                this.setTheme(e.matches ? 'dark' : 'light');
            }
        });

        // Add theme toggle functionality
        this.setupThemeToggle();
        
        // Apply theme-specific animations
        this.applyThemeAnimations();
    }

    setTheme(theme) {
        if (this.currentTheme === theme) return;
        
        this.currentTheme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        this.updateThemeToggle();
        this.updateMetaThemeColor();
        this.dispatchThemeChange();
    }

    updateThemeToggle() {
        const themeToggle = document.getElementById('themeToggle');
        if (!themeToggle) return;

        const icon = themeToggle.querySelector('i');
        if (this.currentTheme === 'dark') {
            icon.className = 'fas fa-sun';
            themeToggle.title = 'Switch to Light Mode';
            themeToggle.setAttribute('aria-label', 'Switch to Light Mode');
        } else {
            icon.className = 'fas fa-moon';
            themeToggle.title = 'Switch to Dark Mode';
            themeToggle.setAttribute('aria-label', 'Switch to Dark Mode');
        }
    }

    updateMetaThemeColor() {
        let metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (!metaThemeColor) {
            metaThemeColor = document.createElement('meta');
            metaThemeColor.name = 'theme-color';
            document.head.appendChild(metaThemeColor);
        }
        
        metaThemeColor.content = this.currentTheme === 'dark' ? '#121212' : '#ffffff';
    }

    setupThemeToggle() {
        // Wait for DOM to be ready
        const setupToggle = () => {
            const themeToggle = document.getElementById('themeToggle');
            if (themeToggle) {
                themeToggle.addEventListener('click', () => {
                    this.toggleTheme();
                });
            } else {
                // Retry after a short delay
                setTimeout(setupToggle, 100);
            }
        };
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', setupToggle);
        } else {
            setupToggle();
        }
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
        
        // Add visual feedback
        this.addToggleAnimation();
    }

    addToggleAnimation() {
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.style.transform = 'scale(0.9)';
            setTimeout(() => {
                themeToggle.style.transform = 'scale(1)';
            }, 150);
        }
    }

    applyThemeAnimations() {
        // Add smooth transitions for theme changes
        const style = document.createElement('style');
        style.textContent = `
            *, *::before, *::after {
                transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease !important;
            }
            
            .hero-section, .hero-section::before {
                transition: background 0.5s ease !important;
            }
        `;
        document.head.appendChild(style);
        
        // Remove transitions after theme change is complete
        setTimeout(() => {
            style.remove();
        }, 500);
    }

    dispatchThemeChange() {
        // Dispatch custom event for theme change
        const event = new CustomEvent('themeChanged', {
            detail: { theme: this.currentTheme }
        });
        document.dispatchEvent(event);
    }

    getCurrentTheme() {
        return this.currentTheme;
    }

    isDarkMode() {
        return this.currentTheme === 'dark';
    }
}

// Enhanced Dark Mode Image Handling
class DarkModeImageManager {
    constructor() {
        this.images = new Map();
        this.init();
    }

    init() {
        this.scanImages();
        document.addEventListener('themeChanged', (e) => {
            this.updateImages(e.detail.theme);
        });
    }

    scanImages() {
        const images = document.querySelectorAll('img[data-dark-src], img[data-light-src]');
        images.forEach(img => {
            const lightSrc = img.getAttribute('data-light-src') || img.src;
            const darkSrc = img.getAttribute('data-dark-src') || img.src;
            
            this.images.set(img, { light: lightSrc, dark: darkSrc });
        });
    }

    updateImages(theme) {
        this.images.forEach((sources, img) => {
            const newSrc = theme === 'dark' ? sources.dark : sources.light;
            if (img.src !== newSrc) {
                img.src = newSrc;
            }
        });
    }
}

// Enhanced Notification System with Dark Mode Support
class NotificationManager {
    constructor() {
        this.container = null;
        this.init();
    }

    init() {
        this.createContainer();
        document.addEventListener('themeChanged', () => {
            this.updateContainerTheme();
        });
    }

    createContainer() {
        this.container = document.createElement('div');
        this.container.className = 'notification-container';
        this.container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 350px;
        `;
        document.body.appendChild(this.container);
    }

    updateContainerTheme() {
        const notifications = this.container.querySelectorAll('.notification');
        notifications.forEach(notification => {
            this.applyThemeToNotification(notification);
        });
    }

    applyThemeToNotification(notification) {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        if (isDark) {
            notification.style.backgroundColor = 'var(--bg-secondary)';
            notification.style.color = 'var(--text-primary)';
            notification.style.borderColor = 'var(--border-color)';
        } else {
            notification.style.backgroundColor = '#ffffff';
            notification.style.color = '#333333';
            notification.style.borderColor = '#dee2e6';
        }
    }

    show(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification alert alert-${type}`;
        notification.style.cssText = `
            margin-bottom: 10px;
            border: 1px solid;
            border-radius: 8px;
            padding: 12px 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transform: translateX(100%);
            transition: all 0.3s ease;
            cursor: pointer;
        `;
        
        notification.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span>${message}</span>
                <i class="fas fa-times" style="margin-left: 10px; opacity: 0.7;"></i>
            </div>
        `;

        this.applyThemeToNotification(notification);
        this.container.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 10);

        // Auto remove
        const removeNotification = () => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        };

        notification.addEventListener('click', removeNotification);
        if (duration > 0) {
            setTimeout(removeNotification, duration);
        }

        return notification;
    }
}

// Theme-aware particle color updates
function updateParticleColors(theme) {
    const particles = document.querySelectorAll('.particle');
    particles.forEach(particle => {
        if (theme === 'dark') {
            particle.style.backgroundColor = 'rgba(77, 171, 247, 0.1)';
        } else {
            particle.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
        }
    });
}

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

    // Enhanced user experience improvements
    function addScrollAnimations() {
        const animatedElements = document.querySelectorAll('.contact-item, .skill-card, .project-card, .timeline-item');
        
        const scrollObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                        entry.target.style.opacity = '1';
                    }, index * 100);
                    scrollObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        animatedElements.forEach(el => {
            el.style.opacity = '0';
            scrollObserver.observe(el);
        });
    }

    // Enhanced contact info interactions
    function enhanceContactInfo() {
        const contactItems = document.querySelectorAll('.contact-item');
        
        contactItems.forEach(item => {
            item.addEventListener('mouseenter', function() {
                const icon = this.querySelector('.contact-icon');
                if (icon) {
                    icon.style.animation = 'pulse 0.6s ease';
                }
            });
            
            item.addEventListener('mouseleave', function() {
                const icon = this.querySelector('.contact-icon');
                if (icon) {
                    icon.style.animation = '';
                }
            });
            
            // Add click to copy functionality for email and phone
            const emailLink = item.querySelector('a[href^="mailto:"]');
            const phoneLink = item.querySelector('a[href^="tel:"]');
            
            if (emailLink) {
                addCopyToClipboard(emailLink, 'Email address copied to clipboard!');
            }
            
            if (phoneLink) {
                addCopyToClipboard(phoneLink, 'Phone number copied to clipboard!');
            }
        });
    }

    // Copy to clipboard functionality
    function addCopyToClipboard(element, message) {
        element.addEventListener('click', function(e) {
            e.preventDefault();
            
            const text = this.textContent.trim();
            navigator.clipboard.writeText(text).then(() => {
                showNotification(message, 'success');
                
                // Visual feedback
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                this.style.color = 'var(--success-color)';
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.style.color = '';
                }, 2000);
            }).catch(() => {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                showNotification(message, 'success');
            });
        });
    }

    // Enhanced notification system
    function showNotification(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification alert alert-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info'} alert-dismissible fade show`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove
        setTimeout(() => {
            if (notification.parentNode) {
                notification.classList.remove('show');
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }
        }, duration);
    }

    // Enhanced form interactions
    function enhanceFormInteractions() {
        const formInputs = document.querySelectorAll('.form-control');
        
        formInputs.forEach(input => {
            // Add floating label effect
            const label = document.querySelector(`label[for="${input.id}"]`);
            
            if (label) {
                input.addEventListener('focus', function() {
                    label.style.color = 'var(--primary-color)';
                    label.style.transform = 'translateY(-2px)';
                    label.style.transition = 'all 0.3s ease';
                });
                
                input.addEventListener('blur', function() {
                    if (!this.value) {
                        label.style.color = '';
                        label.style.transform = '';
                    }
                });
            }
            
            // Add character counter for textarea
            if (input.tagName.toLowerCase() === 'textarea') {
                const maxLength = input.getAttribute('maxlength');
                if (maxLength) {
                    const counter = document.createElement('small');
                    counter.className = 'form-text text-muted character-counter';
                    counter.style.textAlign = 'right';
                    counter.style.display = 'block';
                    input.parentNode.appendChild(counter);
                    
                    const updateCounter = () => {
                        const count = input.value.length;
                        counter.textContent = `${count}/${maxLength}`;
                        counter.style.color = count > maxLength * 0.9 ? 'var(--warning-color)' : 
                                            count === parseInt(maxLength) ? 'var(--danger-color)' : '';
                    };
                    
                    input.addEventListener('input', updateCounter);
                    updateCounter();
                }
            }
        });
    }

    // Enhanced social links
    function enhanceSocialLinks() {
        const socialLinks = document.querySelectorAll('.social-link');
        
        socialLinks.forEach(link => {
            link.addEventListener('mouseenter', function() {
                this.style.animation = 'bounceIn 0.6s ease';
            });
            
            link.addEventListener('mouseleave', function() {
                this.style.animation = '';
            });
            
            // Add tooltip
            const icon = link.querySelector('i');
            if (icon) {
                let platform = 'Website';
                if (icon.classList.contains('fa-linkedin')) platform = 'LinkedIn';
                else if (icon.classList.contains('fa-github')) platform = 'GitHub';
                else if (icon.classList.contains('fa-twitter')) platform = 'Twitter';
                
                link.setAttribute('title', `Visit my ${platform}`);
                link.setAttribute('data-bs-toggle', 'tooltip');
            }
        });
        
        // Initialize tooltips
        if (typeof bootstrap !== 'undefined') {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    }

    // Enhanced navbar interactions
    function enhanceNavbar() {
        const navbar = document.querySelector('.navbar');
        const navLinks = document.querySelectorAll('.nav-link');
        
        // Add active link indicator
        navLinks.forEach(link => {
            link.addEventListener('mouseenter', function() {
                if (!this.classList.contains('active')) {
                    this.style.transform = 'translateY(-2px)';
                    this.style.transition = 'all 0.3s ease';
                }
            });
            
            link.addEventListener('mouseleave', function() {
                if (!this.classList.contains('active')) {
                    this.style.transform = '';
                }
            });
        });
        
        // Enhanced scroll behavior
        let lastScrollTop = 0;
        window.addEventListener('scroll', debounce(() => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                // Scrolling down
                navbar.style.transform = 'translateY(-100%)';
            } else {
                // Scrolling up
                navbar.style.transform = 'translateY(0)';
            }
            
            lastScrollTop = scrollTop;
        }, 10));
    }

    // Parallax effect for hero section
    function addParallaxEffect() {
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const rate = scrolled * -0.5;
                heroSection.style.transform = `translateY(${rate}px)`;
            });
        }
    }

    // Enhanced project cards
    function enhanceProjectCards() {
        const projectCards = document.querySelectorAll('.project-card');
        
        projectCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                const overlay = this.querySelector('.project-overlay');
                if (overlay) {
                    overlay.style.opacity = '1';
                }
            });
            
            card.addEventListener('mouseleave', function() {
                const overlay = this.querySelector('.project-overlay');
                if (overlay) {
                    overlay.style.opacity = '0';
                }
            });
        });
    }

    // Initialize all enhancements
    addScrollAnimations();
    enhanceContactInfo();
    enhanceFormInteractions();
    enhanceSocialLinks();
    enhanceNavbar();
    addParallaxEffect();
    enhanceProjectCards();

    // Add global click handler for external links
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a[target="_blank"]');
        if (link) {
            // Add a small delay to show click feedback
            link.style.transform = 'scale(0.95)';
            setTimeout(() => {
                link.style.transform = '';
            }, 150);
        }
    });
    
    // Add keyboard navigation enhancements
    document.addEventListener('keydown', function(e) {
        // ESC key to close modals/alerts
        if (e.key === 'Escape') {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(alert => {
                const closeBtn = alert.querySelector('.btn-close');
                if (closeBtn) closeBtn.click();
            });
        }
    });

    // Add performance monitoring
    if ('performance' in window) {
        window.addEventListener('load', function() {
            const loadTime = performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart;
            if (loadTime > 3000) {
                console.warn('Page load time is slow:', loadTime + 'ms');
            }
        });
    }

    // Add error handling for images
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            this.style.display = 'none';
            const placeholder = document.createElement('div');
            placeholder.className = 'image-placeholder d-flex align-items-center justify-content-center';
            placeholder.style.cssText = `
                height: ${this.height || 200}px;
                background: #f8f9fa;
                border: 2px dashed #dee2e6;
                border-radius: 8px;
                color: #6c757d;
            `;
            placeholder.innerHTML = '<i class="fas fa-image fa-2x"></i>';
            this.parentNode.insertBefore(placeholder, this);
        });
    });

    // Initialize enhanced dark mode functionality
    window.themeManager = new ThemeManager();
    window.darkModeImageManager = new DarkModeImageManager();
    window.notificationManager = new NotificationManager();
    
    // Add keyboard shortcut for theme toggle (Ctrl/Cmd + Shift + D)
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'D') {
            e.preventDefault();
            window.themeManager.toggleTheme();
            window.notificationManager.show(
                `Switched to ${window.themeManager.getCurrentTheme()} mode`,
                'success',
                2000
            );
        }
    });
    
    // Apply theme-aware particle effects
    document.addEventListener('themeChanged', function(e) {
        updateParticleColors(e.detail.theme);
    });
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
