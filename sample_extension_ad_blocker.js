// Simple Ad Blocker Extension
// This extension hides common ad elements on web pages

(function() {
    'use strict';
    
    // Common ad selectors
    const adSelectors = [
        '[id*="ad-"]',
        '[class*="ad-"]',
        '[id*="advertisement"]',
        '[class*="advertisement"]',
        'iframe[src*="ads"]',
        'iframe[src*="doubleclick"]',
        '.ad',
        '.ads',
        '.adsbygoogle',
        '#ad',
        '#ads'
    ];
    
    // Function to hide ads
    function hideAds() {
        adSelectors.forEach(selector => {
            try {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    el.style.display = 'none';
                    el.style.visibility = 'hidden';
                });
            } catch (e) {
                // Ignore invalid selectors
            }
        });
    }
    
    // Run on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', hideAds);
    } else {
        hideAds();
    }
    
    // Watch for dynamically added ads
    const observer = new MutationObserver(hideAds);
    observer.observe(document.body || document.documentElement, {
        childList: true,
        subtree: true
    });
    
    console.log('Ad Blocker Extension loaded successfully!');
})();
