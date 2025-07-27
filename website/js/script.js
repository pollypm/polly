// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function () {
  // Mobile Navigation
  initMobileNavigation();

  // Smooth Scrolling
  initSmoothScrolling();

  // Copy to Clipboard
  initCopyToClipboard();

  // Scroll Effects
  initScrollEffects();

  // Terminal Animation
  initTerminalAnimation();
});

// Mobile Navigation
function initMobileNavigation() {
  const hamburger = document.querySelector('.hamburger');
  const navMenu = document.querySelector('.nav-menu');
  const navLinks = document.querySelectorAll('.nav-link');

  if (hamburger && navMenu) {
    hamburger.addEventListener('click', function () {
      hamburger.classList.toggle('active');
      navMenu.classList.toggle('active');
    });

    // Close mobile menu when clicking on a link
    navLinks.forEach(link => {
      link.addEventListener('click', function () {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
      });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', function (e) {
      if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
      }
    });
  }
}

// Smooth Scrolling for anchor links
function initSmoothScrolling() {
  const links = document.querySelectorAll('a[href^="#"]');

  links.forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();

      const targetId = this.getAttribute('href');
      const targetSection = document.querySelector(targetId);

      if (targetSection) {
        const headerOffset = 80;
        const elementPosition = targetSection.offsetTop;
        const offsetPosition = elementPosition - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    });
  });
}

// Copy to Clipboard functionality
function initCopyToClipboard() {
  const copyButtons = document.querySelectorAll('.copy-btn');

  copyButtons.forEach(button => {
    button.addEventListener('click', function () {
      const textToCopy = this.getAttribute('data-clipboard-text');

      if (textToCopy) {
        navigator.clipboard.writeText(textToCopy).then(() => {
          // Show success feedback
          showCopyFeedback(this);
        }).catch(err => {
          console.error('Failed to copy text: ', err);
          // Fallback for older browsers
          fallbackCopyTextToClipboard(textToCopy, this);
        });
      }
    });
  });
}

// Show copy feedback
function showCopyFeedback(button) {
  const originalIcon = button.innerHTML;
  button.innerHTML = '<i class="fas fa-check"></i>';
  button.style.color = '#34c759';

  setTimeout(() => {
    button.innerHTML = originalIcon;
    button.style.color = '';
  }, 2000);
}

// Fallback copy function for older browsers
function fallbackCopyTextToClipboard(text, button) {
  const textArea = document.createElement('textarea');
  textArea.value = text;
  textArea.style.top = '0';
  textArea.style.left = '0';
  textArea.style.position = 'fixed';
  textArea.style.opacity = '0';

  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    const successful = document.execCommand('copy');
    if (successful) {
      showCopyFeedback(button);
    }
  } catch (err) {
    console.error('Fallback: Oops, unable to copy', err);
  }

  document.body.removeChild(textArea);
}

// Scroll Effects
function initScrollEffects() {
  const navbar = document.querySelector('.navbar');
  let lastScrollTop = 0;

  window.addEventListener('scroll', function () {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    // Add/remove navbar background based on scroll position
    if (scrollTop > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }

    // Hide/show navbar based on scroll direction
    if (scrollTop > lastScrollTop && scrollTop > 100) {
      // Scrolling down
      navbar.style.transform = 'translateY(-100%)';
    } else {
      // Scrolling up
      navbar.style.transform = 'translateY(0)';
    }

    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
  });

  // Intersection Observer for animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
      }
    });
  }, observerOptions);

  // Observe elements for animation
  const animateElements = document.querySelectorAll('.feature-card, .command-card, .doc-card, .community-card');
  animateElements.forEach(el => {
    observer.observe(el);
  });
}

// Terminal Animation
function initTerminalAnimation() {
  const terminalLines = document.querySelectorAll('.terminal-line');

  if (terminalLines.length > 0) {
    // Hide all lines initially except the first one
    terminalLines.forEach((line, index) => {
      if (index > 0) {
        line.style.opacity = '0';
        line.style.transform = 'translateY(10px)';
      }
    });

    // Animate lines sequentially
    let delay = 1000;
    terminalLines.forEach((line, index) => {
      if (index > 0) {
        setTimeout(() => {
          line.style.transition = 'all 0.5s ease';
          line.style.opacity = '1';
          line.style.transform = 'translateY(0)';
        }, delay);
        delay += 800;
      }
    });
  }
}

// Utility function to check if element is in viewport
function isInViewport(element) {
  const rect = element.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

// Debounce function for performance
function debounce(func, wait, immediate) {
  let timeout;
  return function executedFunction() {
    const context = this;
    const args = arguments;
    const later = function () {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
}

// Theme toggle (if needed in the future)
function initThemeToggle() {
  const themeToggle = document.querySelector('.theme-toggle');

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      document.body.classList.toggle('dark-theme');

      // Save preference
      const isDark = document.body.classList.contains('dark-theme');
      localStorage.setItem('darkTheme', isDark);
    });

    // Load saved theme preference
    const savedTheme = localStorage.getItem('darkTheme');
    if (savedTheme === 'true') {
      document.body.classList.add('dark-theme');
    }
  }
}

// Analytics tracking (placeholder for future implementation)
function trackEvent(category, action, label) {
  // Placeholder for analytics tracking
  console.log('Event tracked:', { category, action, label });

  // Example: Google Analytics
  // if (typeof gtag !== 'undefined') {
  //     gtag('event', action, {
  //         event_category: category,
  //         event_label: label
  //     });
  // }
}

// Track button clicks
document.addEventListener('click', function (e) {
  // Track GitHub button clicks
  if (e.target.closest('.github-link') || e.target.closest('a[href*="github.com"]')) {
    trackEvent('External Link', 'Click', 'GitHub');
  }

  // Track download button clicks
  if (e.target.closest('.btn-primary')) {
    trackEvent('Button', 'Click', 'Primary CTA');
  }

  // Track copy button clicks
  if (e.target.closest('.copy-btn')) {
    trackEvent('Code', 'Copy', 'Command');
  }
});

// Performance monitoring
function logPerformanceMetrics() {
  if ('performance' in window) {
    window.addEventListener('load', function () {
      setTimeout(() => {
        const perfData = performance.getEntriesByType('navigation')[0];
        console.log('Page Load Time:', perfData.loadEventEnd - perfData.loadEventStart);
        console.log('DOM Content Loaded:', perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart);
        console.log('First Paint:', performance.getEntriesByType('paint')[0]?.startTime);
      }, 0);
    });
  }
}

// Initialize performance monitoring in development
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
  logPerformanceMetrics();
}

// Error handling
window.addEventListener('error', function (e) {
  console.error('JavaScript Error:', e.error);
  // In production, you might want to send this to an error tracking service
});

// Service Worker registration (for future PWA features)
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function () {
    // Uncomment when you have a service worker file
    // navigator.serviceWorker.register('/sw.js')
    //     .then(function(registration) {
    //         console.log('ServiceWorker registration successful');
    //     })
    //     .catch(function(err) {
    //         console.log('ServiceWorker registration failed');
    //     });
  });
}
