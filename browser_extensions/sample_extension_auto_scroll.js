// Auto Scroll Extension
// Press 'S' to start/stop auto-scrolling

(function() {
    'use strict';
    
    let scrolling = false;
    let scrollSpeed = 2;
    let scrollInterval;
    
    function startAutoScroll() {
        if (scrolling) return;
        scrolling = true;
        
        scrollInterval = setInterval(() => {
            window.scrollBy(0, scrollSpeed);
        }, 50);
        
        // Show notification
        showNotification('Auto-scroll started (Press S to stop)');
    }
    
    function stopAutoScroll() {
        if (!scrolling) return;
        scrolling = false;
        
        if (scrollInterval) {
            clearInterval(scrollInterval);
        }
        
        showNotification('Auto-scroll stopped');
    }
    
    function showNotification(message) {
        const notification = document.createElement('div');
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4a90e2;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-family: Arial, sans-serif;
            font-size: 14px;
            z-index: 999999;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 2000);
    }
    
    // Listen for 'S' key
    document.addEventListener('keydown', (e) => {
        if (e.key === 's' || e.key === 'S') {
            if (!scrolling) {
                startAutoScroll();
            } else {
                stopAutoScroll();
            }
        }
    });
    
    console.log('Auto Scroll Extension loaded! Press S to toggle auto-scrolling.');
})();
