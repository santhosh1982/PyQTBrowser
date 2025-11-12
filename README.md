# 🌐 Modern Web Browser

A feature-rich, customizable web browser built with Python and PyQt6.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## ✨ Features

### 🎨 **5 Beautiful Themes**
Switch between Light, Dark, Ocean, Sunset, and Forest themes instantly.

### 🧩 **Extension System**
Load custom JavaScript extensions to enhance functionality. Includes 3 sample extensions:
- Dark Mode
- Auto Scroll
- Ad Blocker

### 📌 **Tab Pinning**
Right-click tabs for powerful management:
- Pin/unpin tabs
- Duplicate tabs
- Close other tabs
- Protected pinned tabs

### 💾 **Session Persistence**
Automatically saves and restores:
- All open tabs
- Pinned tab status
- Tab order
- Works across browser restarts

### 📚 **Core Features**
- Smart bookmarks with SQLite storage
- Browsing history
- Download manager with progress tracking
- Customizable settings (homepage, search engine, downloads)
- Keyboard shortcuts

---

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install PyQt6 PyQt6-WebEngine

# Run the browser
python main.py
```

### First Steps

1. **Try a theme**: Tools → 🎨 Themes → Select theme → Apply
2. **Add extension**: Tools → 🧩 Extensions → Add Extension → Select .js file
3. **Pin a tab**: Right-click any tab → 📍 Pin Tab
4. **Close browser**: Your session is auto-saved!
5. **Reopen**: All tabs restored with pinned status

---

## 📖 Documentation

| Guide | Description |
|-------|-------------|
| [COMPLETE_FEATURES.md](COMPLETE_FEATURES.md) | Full feature list and details |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Quick reference card |
| [TAB_PINNING_GUIDE.md](TAB_PINNING_GUIDE.md) | Tab management guide |
| [SESSION_PERSISTENCE_GUIDE.md](SESSION_PERSISTENCE_GUIDE.md) | Session save/restore details |
| [BROWSER_FEATURES.md](BROWSER_FEATURES.md) | Themes and extensions guide |
| [DEMO_GUIDE.md](DEMO_GUIDE.md) | Step-by-step demo |

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+T` | New Tab |
| `Ctrl+W` | Close Tab |
| `Ctrl+B` | Bookmarks |
| `Ctrl+H` | History |
| `Ctrl+J` | Downloads |
| `Ctrl+D` | Add Bookmark |
| `Ctrl+Q` | Exit |

---

## 🎯 Use Cases

### Daily Workflow
- Pin your email, calendar, and dashboard
- Browse other sites throughout the day
- Close browser - session auto-saves
- Reopen tomorrow - everything restored!

### Development
- Test web applications
- Create custom extensions
- Customize themes
- Debug with extensions

### Research
- Open multiple articles
- Pin important references
- Duplicate tabs for comparison
- Session persists across crashes

---

## 🧪 Testing

```bash
# Test all features
python test_features.py

# Test session persistence
python test_session.py
```

---

## 📁 Project Structure

```
PyQtBrowser/
├── main.py                              # Main browser application
├── browser_data.db                      # Bookmarks & history (auto-created)
├── browser_settings.json                # User preferences (auto-created)
├── browser_session.json                 # Tab session (auto-created)
├── extensions.json                      # Extension config (auto-created)
├── browser_extensions/                  # Extension scripts folder
├── sample_extension_dark_mode.js        # Dark mode extension
├── sample_extension_auto_scroll.js      # Auto scroll extension
├── sample_extension_ad_blocker.js       # Ad blocker extension
├── test_features.py                     # Feature tests
├── test_session.py                      # Session tests
└── Documentation/
    ├── README.md                        # This file
    ├── COMPLETE_FEATURES.md             # Complete feature list
    ├── QUICK_REFERENCE.md               # Quick reference
    ├── TAB_PINNING_GUIDE.md            # Tab pinning guide
    ├── SESSION_PERSISTENCE_GUIDE.md     # Session guide
    ├── BROWSER_FEATURES.md              # Features overview
    ├── DEMO_GUIDE.md                    # Demo walkthrough
    ├── WHATS_NEW.md                     # Changelog
    └── QUICK_START.txt                  # Quick start text
```

---

## 🔧 Technical Details

### Built With
- **Python 3.8+**
- **PyQt6** - GUI framework
- **QWebEngine** - Chromium-based browser engine
- **SQLite** - Database for bookmarks/history
- **JSON** - Configuration storage

### Architecture
- Modular class design
- Manager pattern (Theme, Extension, Session, Settings)
- Event-driven UI
- Persistent storage layer

---

## 🎨 Themes

| Theme | Description | Best For |
|-------|-------------|----------|
| Light | Clean, bright interface | Daytime browsing |
| Dark | Dark gray background | Night browsing, eye strain |
| Ocean | Calming teal colors | Focused work |
| Sunset | Warm orange tones | Cozy browsing |
| Forest | Fresh green palette | Natural feel |

---

## 🧩 Creating Extensions

Extensions are simple JavaScript files:

```javascript
(function() {
    'use strict';
    
    // Your code here
    console.log('Extension loaded!');
    
    // Example: Change all links to blue
    document.querySelectorAll('a').forEach(link => {
        link.style.color = 'blue';
    });
})();
```

Save as `.js` file and load via Tools → Extensions.

---

## 📊 Feature Matrix

| Feature | Status | Persistent | Configurable |
|---------|--------|------------|--------------|
| Themes | ✅ | ✅ | ✅ |
| Extensions | ✅ | ✅ | ✅ |
| Tab Pinning | ✅ | ✅ | ❌ |
| Session Restore | ✅ | ✅ | ❌ |
| Bookmarks | ✅ | ✅ | ❌ |
| History | ✅ | ✅ | ✅ |
| Downloads | ✅ | ❌ | ✅ |

---

## 🛡️ Privacy & Security

- ✅ No telemetry or tracking
- ✅ Local storage only
- ✅ No external data sharing
- ✅ Extension isolation
- ✅ HTTPS preference

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional themes
- More sample extensions
- UI enhancements
- Performance optimizations
- Platform testing (Linux, macOS)

---

## 📝 License

MIT License - feel free to use and modify!

---

## 🎉 Acknowledgments

Built with:
- PyQt6 framework
- Chromium web engine
- Python community

---

## 📞 Support

- 📚 Check documentation in `/Documentation`
- 🧪 Run tests: `python test_features.py`
- 💡 See examples in sample extensions
- 📖 Read guides for detailed help

---

## 🚀 Version History

### v2.0 - Complete Package
- ✅ 5 themes with instant switching
- ✅ Extension system with 3 samples
- ✅ Tab pinning with context menu
- ✅ Session persistence with auto-restore
- ✅ Complete documentation
- ✅ Test suite

### v1.0 - Initial Release
- Basic browser functionality
- Bookmarks and history
- Download manager
- Settings

---

**Enjoy your modern, customizable browsing experience!** 🌐✨

*Made with ❤️ using Python and PyQt6*
