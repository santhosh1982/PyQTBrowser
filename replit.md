# Modern Web Browser

## Overview
A fully-featured web browser application built with Python and Qt framework (PyQt6). The browser includes all essential features you'd expect from a modern web browser, including tabbed browsing, bookmarks, history tracking, downloads, and customizable settings.

## Features
- **Multi-tab browsing**: Open, close, and switch between multiple tabs
- **Navigation controls**: Back, forward, reload, and home buttons
- **Smart address bar**: Enter URLs or search terms directly
- **Bookmark management**: Save, view, and organize your favorite pages
- **Browsing history**: Track and revisit previously visited pages
- **Download manager**: Monitor and manage file downloads
- **Customizable settings**: Configure homepage, search engine, and download location
- **Keyboard shortcuts**: Quick access to common functions (Ctrl+T, Ctrl+W, Ctrl+D, etc.)
- **Search integration**: Choose from Google, DuckDuckGo, or Bing

## Technology Stack
- **Language**: Python 3.11
- **GUI Framework**: PyQt6
- **Web Engine**: QtWebEngine (Chromium-based)
- **Database**: SQLite (for bookmarks and history)
- **Configuration**: JSON (for settings)

## Project Structure
- `main.py`: Main application file containing all browser functionality
  - `BrowserDatabase`: Handles bookmark and history storage
  - `SettingsManager`: Manages browser settings
  - `Browser`: Main browser window with tab management
  - `BrowserTab`: Individual browser tab implementation
  - `DownloadManager`: Handles file downloads
  - `BookmarkDialog`, `HistoryDialog`, `SettingsDialog`: UI dialogs

## Keyboard Shortcuts
- `Ctrl+T`: New tab
- `Ctrl+W`: Close current tab
- `Ctrl+D`: Bookmark current page
- `Ctrl+B`: View bookmarks
- `Ctrl+H`: View history
- `Ctrl+J`: View downloads
- `Ctrl+Q`: Quit browser

## Recent Changes
- 2025-11-12: Initial browser implementation with all core features
- Complete multi-tab browsing system
- Bookmark and history management with SQLite database
- Download manager with progress tracking
- Settings panel for customization
- Menu system with keyboard shortcuts

## User Preferences
None specified yet.

## Notes
- The browser uses QtWebEngine which is based on Chromium, providing full support for modern web standards
- Bookmarks and history are stored in a local SQLite database (browser_data.db)
- Settings are saved in a JSON file (browser_settings.json)
- Downloads are saved to ~/Downloads by default (configurable in settings)
