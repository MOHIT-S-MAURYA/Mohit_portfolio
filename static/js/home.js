/* ===== HOME PAGE JAVASCRIPT ===== */

document.addEventListener('DOMContentLoaded', function() {
    // Animated counter for hero stats
    function animateCounters() {
        const counters = document.querySelectorAll('.stat-number[data-count]');
        
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-count'));
            const increment = target / 50;
            let current = 0;
            
            const timer = setInterval(() => {
                current += increment;
                counter.textContent = Math.floor(current);
                
                if (current >= target) {
                    counter.textContent = target;
                    clearInterval(timer);
                }
            }, 40);
        });
    }
    
    // Enhanced typing effect
    function typeWriter() {
        const element = document.querySelector('.typing-cursor');
        if (element) {
            const text = element.textContent;
            element.textContent = '';
            element.classList.remove('typing-cursor');
            
            let i = 0;
            const timer = setInterval(() => {
                element.textContent += text.charAt(i);
                i++;
                
                if (i >= text.length) {
                    clearInterval(timer);
                    element.classList.add('typing-cursor');
                }
            }, 100);
        }
    }
    
    // Start animations after a delay
    setTimeout(typeWriter, 1000);
    setTimeout(animateCounters, 2000);
    
    // Enhanced particle animation
    function createFloatingParticle() {
        const particleContainer = document.querySelector('.hero-particles');
        if (!particleContainer) return;
        
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            left: ${Math.random() * 100}%;
            top: 100%;
            width: ${Math.random() * 4 + 2}px;
            height: ${Math.random() * 4 + 2}px;
            animation: floatUp ${Math.random() * 10 + 10}s linear infinite;
        `;
        
        particleContainer.appendChild(particle);
        
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 20000);
    }
    
    // Add floating particles periodically
    setInterval(createFloatingParticle, 3000);
    
    // Scroll-triggered animations
    function initScrollAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        // Observe elements for animation
        const animatableElements = document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right');
        animatableElements.forEach(el => {
            observer.observe(el);
        });
    }
    
    // Initialize scroll animations
    initScrollAnimations();
    
    // Smooth scrolling for anchor links
    function initSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                const target = document.querySelector(href);
                
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    // Initialize smooth scrolling
    initSmoothScrolling();
    
    // Enhanced hero image effects
    function initHeroImageEffects() {
        const heroImage = document.querySelector('.profile-img');
        if (heroImage) {
            heroImage.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.05) rotate(2deg)';
            });
            
            heroImage.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1) rotate(0deg)';
            });
        }
    }
    
    // Initialize hero image effects
    initHeroImageEffects();
    
    // Social link hover effects
    function initSocialLinkEffects() {
        const socialLinks = document.querySelectorAll('.social-link');
        socialLinks.forEach(link => {
            link.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px) scale(1.1)';
            });
            
            link.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
    }
    
    // Initialize social link effects
    initSocialLinkEffects();
    
    // Page performance monitoring
    function trackPagePerformance() {
        if ('performance' in window) {
            window.addEventListener('load', function() {
                setTimeout(function() {
                    const perfData = window.performance.timing;
                    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
                    console.log('Home page loaded in:', pageLoadTime + 'ms');
                }, 0);
            });
        }
    }
    
    // Track performance
    trackPagePerformance();
});

// Export functions for potential external use
window.HomePageUtils = {
    animateCounters: function() {
        // Implementation here
    },
    createParticle: function() {
        // Implementation here
    }
};
