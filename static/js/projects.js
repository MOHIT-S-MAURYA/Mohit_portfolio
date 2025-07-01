/* ===== PROJECTS PAGE JAVASCRIPT ===== */

document.addEventListener('DOMContentLoaded', function() {
    const projectItems = document.querySelectorAll('.project-item');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const searchInput = document.getElementById('projectSearch');
    const projectsGrid = document.getElementById('projectsGrid');
    const noResults = document.getElementById('noResults');
    
    // Initialize filter counts
    updateFilterCounts();
    
    // Filter functionality
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Update active filter button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            const filter = this.getAttribute('data-filter');
            filterProjects(filter, searchInput ? searchInput.value : '');
            
            // Track filter usage
            if (typeof gtag !== 'undefined') {
                gtag('event', 'filter_projects', {
                    'event_category': 'interaction',
                    'event_label': filter
                });
            }
        });
    });
    
    // Search functionality with debouncing
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function() {
            const activeFilter = document.querySelector('.filter-btn.active')?.getAttribute('data-filter') || 'all';
            filterProjects(activeFilter, this.value);
            
            // Track search usage
            if (typeof gtag !== 'undefined' && this.value.length > 2) {
                gtag('event', 'search_projects', {
                    'event_category': 'interaction',
                    'event_label': this.value
                });
            }
        }, 300));
    }
    
    // Filter projects function
    function filterProjects(filter, searchTerm) {
        let visibleCount = 0;
        const searchTermLower = searchTerm.toLowerCase();
        
        projectItems.forEach((item, index) => {
            const category = item.getAttribute('data-category') || '';
            const title = item.getAttribute('data-title') || '';
            const tech = item.getAttribute('data-tech') || '';
            const description = item.getAttribute('data-description') || '';
            
            const matchesFilter = filter === 'all' || category.includes(filter);
            const matchesSearch = !searchTerm || 
                                title.toLowerCase().includes(searchTermLower) || 
                                tech.toLowerCase().includes(searchTermLower) ||
                                description.toLowerCase().includes(searchTermLower);
            
            if (matchesFilter && matchesSearch) {
                showProjectItem(item, index);
                visibleCount++;
            } else {
                hideProjectItem(item);
            }
        });
        
        // Show/hide no results message
        updateResultsDisplay(visibleCount);
        
        // Update filter counts after filtering
        updateFilterCounts();
    }
    
    // Show project item with animation
    function showProjectItem(item, index) {
        item.style.display = 'block';
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            item.style.animation = 'fadeInUp 0.5s ease forwards';
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, index * 50);
    }
    
    // Hide project item
    function hideProjectItem(item) {
        item.style.animation = 'fadeOut 0.3s ease forwards';
        setTimeout(() => {
            item.style.display = 'none';
        }, 300);
    }
    
    // Update results display
    function updateResultsDisplay(visibleCount) {
        if (noResults && projectsGrid) {
            if (visibleCount === 0) {
                noResults.style.display = 'block';
                projectsGrid.style.display = 'none';
                noResults.style.animation = 'fadeIn 0.5s ease forwards';
            } else {
                noResults.style.display = 'none';
                projectsGrid.style.display = 'flex';
            }
        }
    }
    
    // Update filter counts
    function updateFilterCounts() {
        const visibleProjects = Array.from(projectItems).filter(item => 
            item.style.display !== 'none'
        );
        
        const webCount = visibleProjects.filter(item => 
            item.getAttribute('data-category')?.includes('web')
        ).length;
        
        const mobileCount = visibleProjects.filter(item => 
            item.getAttribute('data-category')?.includes('mobile')
        ).length;
        
        const webCountElement = document.getElementById('web-count');
        const mobileCountElement = document.getElementById('mobile-count');
        
        if (webCountElement) webCountElement.textContent = webCount;
        if (mobileCountElement) mobileCountElement.textContent = mobileCount;
    }
    
    // Clear filters function
    window.clearFilters = function() {
        if (searchInput) searchInput.value = '';
        filterButtons.forEach(btn => btn.classList.remove('active'));
        const allButton = document.querySelector('[data-filter="all"]');
        if (allButton) allButton.classList.add('active');
        filterProjects('all', '');
    };
    
    // Enhanced project card interactions
    function initProjectCardEffects() {
        projectItems.forEach(item => {
            const card = item.querySelector('.project-card');
            if (!card) return;
            
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-15px) rotateX(8deg) scale(1.02)';
                this.style.boxShadow = '0 25px 50px rgba(0, 0, 0, 0.25)';
                
                // Add glow effect
                const overlay = this.querySelector('.project-overlay');
                if (overlay) {
                    overlay.style.opacity = '0.95';
                }
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) rotateX(0) scale(1)';
                this.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.15)';
                
                const overlay = this.querySelector('.project-overlay');
                if (overlay) {
                    overlay.style.opacity = '0.8';
                }
            });
            
            // Add click tracking
            card.addEventListener('click', function() {
                const projectTitle = item.getAttribute('data-title') || 'Unknown';
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'project_view', {
                        'event_category': 'engagement',
                        'event_label': projectTitle
                    });
                }
            });
        });
    }
    
    // Lazy loading for images
    function initLazyLoading() {
        const images = document.querySelectorAll('img[loading="lazy"]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.classList.add('loaded');
                    
                    // Add fade-in effect
                    img.style.opacity = '0';
                    img.style.transition = 'opacity 0.5s ease';
                    
                    img.onload = function() {
                        this.style.opacity = '1';
                    };
                    
                    imageObserver.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.1
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
    
    // Scroll animations for projects
    function initScrollAnimations() {
        const animateOnScroll = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.animation = 'fadeInUp 0.8s ease forwards';
                        entry.target.style.opacity = '1';
                    }, index * 100);
                    animateOnScroll.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        projectItems.forEach(item => {
            item.style.opacity = '0';
            animateOnScroll.observe(item);
        });
    }
    
    // Tech tag hover effects
    function initTechTagEffects() {
        const techTags = document.querySelectorAll('.tech-tag');
        techTags.forEach(tag => {
            tag.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.1)';
                this.style.boxShadow = '0 5px 15px rgba(102, 126, 234, 0.3)';
            });
            
            tag.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
                this.style.boxShadow = 'none';
            });
        });
    }
    
    // Initialize URL-based filtering
    function initURLFiltering() {
        const urlParams = new URLSearchParams(window.location.search);
        const filterParam = urlParams.get('filter');
        const searchParam = urlParams.get('search');
        
        if (filterParam) {
            const filterButton = document.querySelector(`[data-filter="${filterParam}"]`);
            if (filterButton) {
                filterButtons.forEach(btn => btn.classList.remove('active'));
                filterButton.classList.add('active');
            }
        }
        
        if (searchParam && searchInput) {
            searchInput.value = searchParam;
        }
        
        // Apply initial filters
        const activeFilter = document.querySelector('.filter-btn.active')?.getAttribute('data-filter') || 'all';
        filterProjects(activeFilter, searchParam || '');
    }
    
    // Update URL when filters change
    function updateURL(filter, search) {
        const url = new URL(window.location);
        if (filter && filter !== 'all') {
            url.searchParams.set('filter', filter);
        } else {
            url.searchParams.delete('filter');
        }
        
        if (search) {
            url.searchParams.set('search', search);
        } else {
            url.searchParams.delete('search');
        }
        
        window.history.replaceState({}, '', url.toString());
    }
    
    // Initialize all functionality
    function init() {
        initProjectCardEffects();
        initLazyLoading();
        initScrollAnimations();
        initTechTagEffects();
        initURLFiltering();
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
                    console.log('Projects page loaded in:', pageLoadTime + 'ms');
                }, 0);
            });
        }
    }
    
    trackPagePerformance();
});

// Utility function for debouncing
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

// Add required CSS animations
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
    
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: scale(1);
        }
        to {
            opacity: 0;
            transform: scale(0.9);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    .project-card {
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
`;
document.head.appendChild(style);

// Export utilities for external use
window.ProjectsPageUtils = {
    filterProjects: function(filter, search) {
        // Public method for filtering
    },
    clearFilters: function() {
        if (typeof clearFilters === 'function') {
            clearFilters();
        }
    }
};
