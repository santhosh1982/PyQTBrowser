// Dark Mode Extension for Browser
// This extension inverts colors on web pages for a dark mode effect

(function() {
    'use strict';
    
    // Create a style element for dark mode
    const style = document.createElement('style');
    style.id = 'dark-mode-extension';
    style.textContent = `
        html {
            filter: invert(0.9) hue-rotate(180deg) !important;
            background-color: #1a1a1a !important;
        }
        
        img, video, iframe, [style*="background-image"] {
            filter: invert(1) hue-rotate(180deg) !important;
        }
    `;
    
    // Add the style to the document
    if (document.head) {
        document.head.appendChild(style);
    } else {
        document.addEventListener('DOMContentLoaded', function() {
            document.head.appendChild(style);
        });
    }
    
    console.log('Dark Mode Extension loaded successfully!');
})();
