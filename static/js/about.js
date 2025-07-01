/* ===== ABOUT PAGE JAVASCRIPT ===== */

document.addEventListener('DOMContentLoaded', function() {
    // Animated counters for stats
    function animateCounters() {
        const counters = document.querySelectorAll('.stat-number[data-count]');
        
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
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
                    }, 30);
                    
                    counterObserver.unobserve(counter);
                }
            });
        }, {
            threshold: 0.5
        });
        
        counters.forEach(counter => counterObserver.observe(counter));
    }
    
    // Animate skill progress bars
    function animateSkillBars() {
        const skillBars = document.querySelectorAll('.skill-progress-bar');
        
        const skillObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const bar = entry.target;
                    const width = bar.getAttribute('data-width');
                    
                    setTimeout(() => {
                        bar.style.width = width;
                    }, 200);
                    
                    skillObserver.unobserve(bar);
                }
            });
        }, {
            threshold: 0.3
        });
        
        skillBars.forEach(bar => skillObserver.observe(bar));
    }
    
    // Scroll animations for timeline items
    function animateTimelineItems() {
        const timelineItems = document.querySelectorAll('.timeline-item-enhanced');
        
        const timelineObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.animation = 'fadeInUp 0.8s ease forwards';
                        entry.target.style.opacity = '1';
                    }, index * 200);
                    
                    timelineObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.2
        });
        
        timelineItems.forEach(item => {
            item.style.opacity = '0';
            timelineObserver.observe(item);
        });
    }
    
    // Scroll animations for other elements
    function addScrollAnimations() {
        const animatedElements = document.querySelectorAll('.skill-category, .stats-card, .animate-in');
        
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
            threshold: 0.1
        });
        
        animatedElements.forEach(el => {
            el.style.opacity = '0';
            scrollObserver.observe(el);
        });
    }
    
    // Enhanced hover effects for skill items
    function enhanceSkillInteractions() {
        const skillItems = document.querySelectorAll('.skill-item');
        
        skillItems.forEach(item => {
            item.addEventListener('mouseenter', function() {
                const bar = this.querySelector('.skill-progress-bar');
                if (bar) {
                    bar.style.background = 'linear-gradient(45deg, var(--brand-primary), var(--color-success))';
                    bar.style.boxShadow = '0 2px 10px rgba(102, 126, 234, 0.3)';
                }
                
                // Add subtle pulse effect
                this.style.transform = 'translateX(10px) scale(1.02)';
            });
            
            item.addEventListener('mouseleave', function() {
                const bar = this.querySelector('.skill-progress-bar');
                if (bar) {
                    bar.style.background = 'linear-gradient(45deg, var(--brand-primary), var(--brand-primary-dark))';
                    bar.style.boxShadow = 'none';
                }
                
                this.style.transform = 'translateX(5px) scale(1)';
            });
        });
    }
    
    // Parallax effect for hero section
    function initParallaxEffects() {
        const heroSection = document.querySelector('.about-hero');
        if (!heroSection) return;
        
        let ticking = false;
        
        function updateParallax() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.3;
            heroSection.style.transform = `translateY(${rate}px)`;
            ticking = false;
        }
        
        function requestTick() {
            if (!ticking) {
                requestAnimationFrame(updateParallax);
                ticking = true;
            }
        }
        
        window.addEventListener('scroll', requestTick);
    }
    
    // Enhanced profile image interactions
    function initProfileImageEffects() {
        const profileImage = document.querySelector('.profile-image');
        if (profileImage) {
            profileImage.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-10px) scale(1.05) rotate(2deg)';
            });
            
            profileImage.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1) rotate(0deg)';
            });
        }
    }
    
    // Download CV button effects
    function initDownloadCVEffects() {
        const downloadBtn = document.querySelector('.download-cv');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', function(e) {
                // Add click animation
                this.style.transform = 'translateY(0) scale(0.95)';
                
                setTimeout(() => {
                    this.style.transform = 'translateY(-3px) scale(1)';
                }, 150);
                
                // Track download event
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'cv_download', {
                        'event_category': 'engagement',
                        'event_label': 'CV Download from About Page'
                    });
                }
            });
        }
    }
    
    // Stats card hover effects
    function initStatsCardEffects() {
        const statsCards = document.querySelectorAll('.stats-card');
        statsCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-10px) scale(1.05)';
                this.style.boxShadow = '0 20px 40px rgba(102, 126, 234, 0.2)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.1)';
            });
        });
    }
    
    // Timeline marker animations
    function initTimelineMarkerEffects() {
        const markers = document.querySelectorAll('.timeline-marker-enhanced');
        
        const markerObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'pulse 2s ease-in-out infinite';
                    markerObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.5
        });
        
        markers.forEach(marker => markerObserver.observe(marker));
    }
    
    // Initialize all functions
    function init() {
        animateCounters();
        animateSkillBars();
        animateTimelineItems();
        addScrollAnimations();
        enhanceSkillInteractions();
        initParallaxEffects();
        initProfileImageEffects();
        initDownloadCVEffects();
        initStatsCardEffects();
        initTimelineMarkerEffects();
    }
    
    // Start initialization
    init();
    
    // Smooth scrolling for internal links
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    internalLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Performance monitoring
    function trackPagePerformance() {
        if ('performance' in window) {
            window.addEventListener('load', function() {
                setTimeout(function() {
                    const perfData = window.performance.timing;
                    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
                    console.log('About page loaded in:', pageLoadTime + 'ms');
                }, 0);
            });
        }
    }
    
    trackPagePerformance();
});

// Add required CSS animations dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(102, 126, 234, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(102, 126, 234, 0);
        }
    }
`;
document.head.appendChild(style);

// Export utilities for external use
window.AboutPageUtils = {
    animateCounters: function() {
        // Public method for counter animation
    },
    animateSkillBars: function() {
        // Public method for skill bar animation
    }
};
