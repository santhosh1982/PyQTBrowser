# Modern Web Browser - Themes & Extensions Guide

## 🎨 Themes

Your browser now includes 5 beautiful built-in themes:

### Available Themes:
1. **Light** - Clean, bright interface (default)
2. **Dark** - Easy on the eyes for night browsing
3. **Ocean** - Calming teal and aqua colors
4. **Sunset** - Warm orange and amber tones
5. **Forest** - Fresh green nature-inspired palette

### How to Change Themes:
1. Go to **Tools → 🎨 Themes** in the menu bar
2. Select your preferred theme from the list
3. Click **✓ Apply Theme**
4. Your theme will be saved and applied immediately!

## 🧩 Extensions

Add custom functionality to your browser with JavaScript extensions!

### Managing Extensions:
1. Go to **Tools → 🧩 Extensions** in the menu bar
2. Click **➕ Add Extension** to add a new extension
3. Select a JavaScript (.js) file
4. Give your extension a name
5. Toggle extensions on/off with **🔄 Toggle Enable/Disable**
6. Remove extensions with **🗑️ Remove**

### Sample Extensions Included:

#### 1. Dark Mode Extension (`sample_extension_dark_mode.js`)
- Inverts colors on all web pages for a dark mode effect
- Great for reducing eye strain at night
- Works on any website

#### 2. Auto Scroll Extension (`sample_extension_auto_scroll.js`)
- Press **'S'** key to start/stop auto-scrolling
- Perfect for reading long articles
- Adjustable scroll speed

#### 3. Ad Blocker Extension (`sample_extension_ad_blocker.js`)
- Hides common advertisement elements
- Blocks ads dynamically as they load
- Cleaner browsing experience

### Creating Your Own Extensions:

Extensions are simple JavaScript files that run on every page. Here's a basic template:

```javascript
(function() {
    'use strict';
    
    // Your extension code here
    console.log('My extension loaded!');
    
    // Example: Change all links to blue
    document.querySelectorAll('a').forEach(link => {
        link.style.color = 'blue';
    });
})();
```

### Extension Tips:
- Extensions run when the page is ready (DocumentReady)
- Use `console.log()` to debug your extensions
- Extensions persist across browser restarts
- Disabled extensions won't run but remain in your list

## 🚀 Quick Start

1. **Try a theme**: Tools → Themes → Select "Dark" or "Ocean"
2. **Add an extension**: Tools → Extensions → Add Extension → Select `sample_extension_auto_scroll.js`
3. **Test it**: Visit any website and press 'S' to auto-scroll!

## 💡 Pro Tips

- **Theme switching**: Themes apply instantly without restarting
- **Extension debugging**: Check the browser console for extension logs
- **Performance**: Disable unused extensions for better performance
- **Customization**: Edit sample extensions to create your own variations

Enjoy your enhanced browsing experience! 🎉
