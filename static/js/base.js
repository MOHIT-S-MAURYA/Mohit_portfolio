// Base Template Global Scripts
// This file handles global functionality for the base template

// Page loader functionality
window.addEventListener('load', function() {
    const loader = document.getElementById('pageLoader');
    if (loader) {
        loader.style.opacity = '0';
        setTimeout(() => {
            loader.style.display = 'none';
        }, 300);
    }
});

// Progress bar functionality
window.addEventListener('scroll', function() {
    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
        const scrollTop = document.documentElement.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrollPercent = (scrollTop / scrollHeight) * 100;
        progressBar.style.width = scrollPercent + '%';
    }
});

// Scroll to top functionality
const scrollToTop = document.getElementById('scrollToTop');
if (scrollToTop) {
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollToTop.classList.add('visible');
        } else {
            scrollToTop.classList.remove('visible');
        }
    });
    
    scrollToTop.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// Fallback theme toggle in case of script issues
const fallbackThemeToggle = () => {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle && !window.themeManager) {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
        
        function setTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            
            const icon = themeToggle.querySelector('i');
            if (theme === 'dark') {
                icon.className = 'fas fa-sun';
                themeToggle.title = 'Switch to Light Mode';
            } else {
                icon.className = 'fas fa-moon';
                themeToggle.title = 'Switch to Dark Mode';
            }
        }
        
        // Initialize theme
        const savedTheme = localStorage.getItem('theme') || (prefersDark.matches ? 'dark' : 'light');
        setTheme(savedTheme);
        
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            setTheme(currentTheme === 'dark' ? 'light' : 'dark');
        });
    }
};

// Try fallback after a delay
setTimeout(fallbackThemeToggle, 1000);

// Privacy modal functionality
function showPrivacyModal() {
    const modal = new bootstrap.Modal(document.getElementById('privacyModal') || createPrivacyModal());
    modal.show();
}

function createPrivacyModal() {
    const modalHTML = `
        <div class="modal fade" id="privacyModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Privacy Policy</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>This website respects your privacy and is committed to protecting your personal information.</p>
                        <h6>Information We Collect</h6>
                        <p>We only collect information you voluntarily provide through our contact form.</p>
                        <h6>How We Use Your Information</h6>
                        <p>We use your information solely to respond to your inquiries and communicate with you about potential projects.</p>
                        <h6>Data Security</h6>
                        <p>We implement appropriate security measures to protect your personal information.</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    return document.getElementById('privacyModal');
}

// Make privacy modal function globally available
window.showPrivacyModal = showPrivacyModal;
