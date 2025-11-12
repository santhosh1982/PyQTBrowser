import sys
import os
import json
import sqlite3
from datetime import datetime
from PyQt6.QtCore import QUrl, Qt, QSize, QTimer
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QToolBar, 
                              QLineEdit, QPushButton, QVBoxLayout, QWidget, 
                              QHBoxLayout, QDialog, QListWidget, QLabel, 
                              QMessageBox, QInputDialog, QMenu, QFileDialog,
                              QProgressBar, QListWidgetItem, QComboBox)
from PyQt6.QtGui import QIcon, QAction, QKeySequence
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest, QWebEngineProfile


class BrowserDatabase:
    def __init__(self):
        self.db_path = 'browser_data.db'
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                visited_at TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_bookmark(self, title, url):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bookmarks (title, url, created_at) VALUES (?, ?, ?)',
                      (title, url, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_bookmarks(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, url, created_at FROM bookmarks ORDER BY created_at DESC')
        bookmarks = cursor.fetchall()
        conn.close()
        return bookmarks
    
    def delete_bookmark(self, bookmark_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bookmarks WHERE id = ?', (bookmark_id,))
        conn.commit()
        conn.close()
    
    def add_history(self, title, url):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO history (title, url, visited_at) VALUES (?, ?, ?)',
                      (title, url, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_history(self, limit=100):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, url, visited_at FROM history ORDER BY visited_at DESC LIMIT ?', (limit,))
        history = cursor.fetchall()
        conn.close()
        return history
    
    def clear_history(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM history')
        conn.commit()
        conn.close()


class SettingsManager:
    def __init__(self):
        self.settings_file = 'browser_settings.json'
        self.default_settings = {
            'homepage': 'https://www.google.com',
            'search_engine': 'https://www.google.com/search?q=',
            'download_path': os.path.expanduser('~/Downloads')
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        return self.default_settings.copy()
    
    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def get(self, key):
        return self.settings.get(key, self.default_settings.get(key))
    
    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()


class BrowserTab(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_browser = parent
        
    def createWindow(self, window_type):
        new_tab = self.parent_browser.add_new_tab(QUrl('about:blank'), 'New Tab')
        return new_tab


class DownloadManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Download Manager')
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        self.download_list = QListWidget()
        layout.addWidget(QLabel('Active Downloads:'))
        layout.addWidget(self.download_list)
        
        self.setLayout(layout)
        self.downloads = {}
    
    def add_download(self, download_item, file_path):
        item_widget = QWidget()
        item_layout = QVBoxLayout()
        
        name_label = QLabel(f"File: {os.path.basename(file_path)}")
        progress_bar = QProgressBar()
        progress_bar.setMaximum(100)
        
        item_layout.addWidget(name_label)
        item_layout.addWidget(progress_bar)
        item_widget.setLayout(item_layout)
        
        list_item = QListWidgetItem(self.download_list)
        list_item.setSizeHint(item_widget.sizeHint())
        self.download_list.addItem(list_item)
        self.download_list.setItemWidget(list_item, item_widget)
        
        self.downloads[download_item] = {
            'progress_bar': progress_bar,
            'list_item': list_item,
            'name_label': name_label
        }
        
        download_item.receivedBytesChanged.connect(
            lambda: self.update_progress(download_item)
        )
        download_item.isFinishedChanged.connect(
            lambda: self.download_finished(download_item)
        )
    
    def update_progress(self, download_item):
        if download_item in self.downloads:
            received = download_item.receivedBytes()
            total = download_item.totalBytes()
            if total > 0:
                progress = int((received / total) * 100)
                self.downloads[download_item]['progress_bar'].setValue(progress)
    
    def download_finished(self, download_item):
        if download_item in self.downloads:
            if download_item.isFinished():
                self.downloads[download_item]['progress_bar'].setValue(100)
                self.downloads[download_item]['name_label'].setText(
                    f"✓ {self.downloads[download_item]['name_label'].text()[6:]}"
                )


class BookmarkDialog(QDialog):
    def __init__(self, database, parent=None):
        super().__init__(parent)
        self.database = database
        self.setWindowTitle('Bookmarks')
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel('Your Bookmarks:'))
        
        self.bookmark_list = QListWidget()
        self.bookmark_list.itemDoubleClicked.connect(self.open_bookmark)
        layout.addWidget(self.bookmark_list)
        
        button_layout = QHBoxLayout()
        delete_btn = QPushButton('Delete Selected')
        delete_btn.clicked.connect(self.delete_bookmark)
        button_layout.addWidget(delete_btn)
        
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.load_bookmarks()
    
    def load_bookmarks(self):
        self.bookmark_list.clear()
        bookmarks = self.database.get_bookmarks()
        for bookmark in bookmarks:
            item = QListWidgetItem(f"{bookmark[1]} - {bookmark[2]}")
            item.setData(Qt.ItemDataRole.UserRole, bookmark)
            self.bookmark_list.addItem(item)
    
    def open_bookmark(self, item):
        bookmark = item.data(Qt.ItemDataRole.UserRole)
        if self.parent():
            self.parent().navigate_to_url(bookmark[2])
        self.close()
    
    def delete_bookmark(self):
        current_item = self.bookmark_list.currentItem()
        if current_item:
            bookmark = current_item.data(Qt.ItemDataRole.UserRole)
            self.database.delete_bookmark(bookmark[0])
            self.load_bookmarks()


class HistoryDialog(QDialog):
    def __init__(self, database, parent=None):
        super().__init__(parent)
        self.database = database
        self.setWindowTitle('Browsing History')
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel('Your Browsing History:'))
        
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.open_history_item)
        layout.addWidget(self.history_list)
        
        button_layout = QHBoxLayout()
        clear_btn = QPushButton('Clear All History')
        clear_btn.clicked.connect(self.clear_history)
        button_layout.addWidget(clear_btn)
        
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.load_history()
    
    def load_history(self):
        self.history_list.clear()
        history = self.database.get_history()
        for item in history:
            list_item = QListWidgetItem(f"{item[1]} - {item[2]} ({item[3][:19]})")
            list_item.setData(Qt.ItemDataRole.UserRole, item)
            self.history_list.addItem(list_item)
    
    def open_history_item(self, item):
        history = item.data(Qt.ItemDataRole.UserRole)
        if self.parent():
            self.parent().navigate_to_url(history[2])
        self.close()
    
    def clear_history(self):
        reply = QMessageBox.question(self, 'Clear History',
                                     'Are you sure you want to clear all browsing history?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.database.clear_history()
            self.load_history()


class SettingsDialog(QDialog):
    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.setWindowTitle('Browser Settings')
        self.setGeometry(100, 100, 500, 300)
        
        layout = QVBoxLayout()
        
        homepage_layout = QHBoxLayout()
        homepage_layout.addWidget(QLabel('Homepage:'))
        self.homepage_input = QLineEdit()
        self.homepage_input.setText(self.settings_manager.get('homepage'))
        homepage_layout.addWidget(self.homepage_input)
        layout.addLayout(homepage_layout)
        
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel('Search Engine:'))
        self.search_combo = QComboBox()
        self.search_combo.addItem('Google', 'https://www.google.com/search?q=')
        self.search_combo.addItem('DuckDuckGo', 'https://duckduckgo.com/?q=')
        self.search_combo.addItem('Bing', 'https://www.bing.com/search?q=')
        
        current_search = self.settings_manager.get('search_engine')
        index = self.search_combo.findData(current_search)
        if index >= 0:
            self.search_combo.setCurrentIndex(index)
        
        search_layout.addWidget(self.search_combo)
        layout.addLayout(search_layout)
        
        download_layout = QHBoxLayout()
        download_layout.addWidget(QLabel('Download Path:'))
        self.download_input = QLineEdit()
        self.download_input.setText(self.settings_manager.get('download_path'))
        download_layout.addWidget(self.download_input)
        browse_btn = QPushButton('Browse')
        browse_btn.clicked.connect(self.browse_download_path)
        download_layout.addWidget(browse_btn)
        layout.addLayout(download_layout)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton('Save')
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton('Cancel')
        cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def browse_download_path(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Download Directory')
        if path:
            self.download_input.setText(path)
    
    def save_settings(self):
        self.settings_manager.set('homepage', self.homepage_input.text())
        self.settings_manager.set('search_engine', self.search_combo.currentData())
        self.settings_manager.set('download_path', self.download_input.text())
        QMessageBox.information(self, 'Settings Saved', 'Your settings have been saved successfully!')
        self.close()


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.database = BrowserDatabase()
        self.settings_manager = SettingsManager()
        self.download_manager = DownloadManager(self)
        
        self.setWindowTitle('Modern Web Browser')
        self.setGeometry(100, 100, 1200, 800)
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)
        
        self.setCentralWidget(self.tabs)
        
        navbar = QToolBar()
        navbar.setMovable(False)
        navbar.setIconSize(QSize(24, 24))
        self.addToolBar(navbar)
        
        back_btn = QAction('←', self)
        back_btn.setToolTip('Back')
        back_btn.triggered.connect(lambda: self.current_browser().back())
        navbar.addAction(back_btn)
        
        forward_btn = QAction('→', self)
        forward_btn.setToolTip('Forward')
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        navbar.addAction(forward_btn)
        
        reload_btn = QAction('⟳', self)
        reload_btn.setToolTip('Reload')
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        navbar.addAction(reload_btn)
        
        home_btn = QAction('⌂', self)
        home_btn.setToolTip('Home')
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)
        
        navbar.addSeparator()
        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        
        navbar.addSeparator()
        
        new_tab_btn = QAction('+', self)
        new_tab_btn.setToolTip('New Tab')
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(QUrl(self.settings_manager.get('homepage')), 'New Tab'))
        navbar.addAction(new_tab_btn)
        
        bookmark_add_btn = QAction('★', self)
        bookmark_add_btn.setToolTip('Bookmark this page')
        bookmark_add_btn.triggered.connect(self.add_bookmark)
        navbar.addAction(bookmark_add_btn)
        
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu('File')
        
        new_tab_action = QAction('New Tab', self)
        new_tab_action.setShortcut(QKeySequence('Ctrl+T'))
        new_tab_action.triggered.connect(lambda: self.add_new_tab(QUrl(self.settings_manager.get('homepage')), 'New Tab'))
        file_menu.addAction(new_tab_action)
        
        close_tab_action = QAction('Close Tab', self)
        close_tab_action.setShortcut(QKeySequence('Ctrl+W'))
        close_tab_action.triggered.connect(lambda: self.close_tab(self.tabs.currentIndex()))
        file_menu.addAction(close_tab_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut(QKeySequence('Ctrl+Q'))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        bookmarks_menu = menu_bar.addMenu('Bookmarks')
        
        add_bookmark_action = QAction('Add Bookmark', self)
        add_bookmark_action.setShortcut(QKeySequence('Ctrl+D'))
        add_bookmark_action.triggered.connect(self.add_bookmark)
        bookmarks_menu.addAction(add_bookmark_action)
        
        view_bookmarks_action = QAction('View Bookmarks', self)
        view_bookmarks_action.setShortcut(QKeySequence('Ctrl+B'))
        view_bookmarks_action.triggered.connect(self.view_bookmarks)
        bookmarks_menu.addAction(view_bookmarks_action)
        
        history_menu = menu_bar.addMenu('History')
        
        view_history_action = QAction('View History', self)
        view_history_action.setShortcut(QKeySequence('Ctrl+H'))
        view_history_action.triggered.connect(self.view_history)
        history_menu.addAction(view_history_action)
        
        clear_history_action = QAction('Clear History', self)
        clear_history_action.triggered.connect(self.clear_history)
        history_menu.addAction(clear_history_action)
        
        tools_menu = menu_bar.addMenu('Tools')
        
        downloads_action = QAction('Downloads', self)
        downloads_action.setShortcut(QKeySequence('Ctrl+J'))
        downloads_action.triggered.connect(self.show_downloads)
        tools_menu.addAction(downloads_action)
        
        settings_action = QAction('Settings', self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
        QWebEngineProfile.defaultProfile().downloadRequested.connect(self.on_download_requested)
        
        self.add_new_tab(QUrl(self.settings_manager.get('homepage')), 'Home')
        
        self.show()
    
    def current_browser(self):
        return self.tabs.currentWidget()
    
    def add_new_tab(self, qurl=None, label='New Tab'):
        if qurl is None:
            qurl = QUrl(self.settings_manager.get('homepage'))
        
        browser = BrowserTab(self)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl, browser))
        browser.loadFinished.connect(lambda _, browser=browser: self.update_title(browser))
        browser.loadProgress.connect(lambda progress: self.update_load_progress(progress))
        
        browser.setUrl(qurl)
        
        return browser
    
    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)
        else:
            self.close()
    
    def navigate_to_url(self, url=None):
        if url is None:
            url = self.url_bar.text()
        else:
            if isinstance(url, str):
                self.url_bar.setText(url)
        
        if not url.startswith('http://') and not url.startswith('https://') and not url.startswith('about:'):
            if '.' in url and ' ' not in url:
                url = 'https://' + url
            else:
                search_engine = self.settings_manager.get('search_engine')
                url = search_engine + url.replace(' ', '+')
        
        self.current_browser().setUrl(QUrl(url))
    
    def navigate_home(self):
        self.navigate_to_url(self.settings_manager.get('homepage'))
    
    def update_url(self, qurl, browser=None):
        if browser != self.current_browser():
            return
        
        self.url_bar.setText(qurl.toString())
        
        title = browser.page().title()
        url = qurl.toString()
        
        if url and url != 'about:blank':
            self.database.add_history(title if title else url, url)
    
    def update_title(self, browser):
        if browser != self.current_browser():
            return
        
        title = browser.page().title()
        i = self.tabs.indexOf(browser)
        
        if len(title) > 20:
            title = title[:20] + '...'
        
        self.tabs.setTabText(i, title if title else 'New Tab')
    
    def update_url_bar(self):
        browser = self.current_browser()
        if browser:
            qurl = browser.url()
            self.url_bar.setText(qurl.toString())
    
    def update_load_progress(self, progress):
        if progress < 100:
            self.setWindowTitle(f'Loading ({progress}%) - Modern Web Browser')
        else:
            self.setWindowTitle('Modern Web Browser')
    
    def add_bookmark(self):
        browser = self.current_browser()
        if browser:
            title = browser.page().title()
            url = browser.url().toString()
            
            if url and url != 'about:blank':
                self.database.add_bookmark(title if title else url, url)
                QMessageBox.information(self, 'Bookmark Added', f'Page "{title}" has been bookmarked!')
    
    def view_bookmarks(self):
        dialog = BookmarkDialog(self.database, self)
        dialog.exec()
    
    def view_history(self):
        dialog = HistoryDialog(self.database, self)
        dialog.exec()
    
    def clear_history(self):
        reply = QMessageBox.question(self, 'Clear History',
                                     'Are you sure you want to clear all browsing history?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.database.clear_history()
            QMessageBox.information(self, 'History Cleared', 'All browsing history has been cleared!')
    
    def show_downloads(self):
        self.download_manager.show()
    
    def show_settings(self):
        dialog = SettingsDialog(self.settings_manager, self)
        dialog.exec()
    
    def on_download_requested(self, download):
        download_path = self.settings_manager.get('download_path')
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        
        suggested_filename = download.downloadFileName()
        file_path = os.path.join(download_path, suggested_filename)
        
        download.setDownloadDirectory(download_path)
        download.setDownloadFileName(suggested_filename)
        download.accept()
        
        self.download_manager.add_download(download, file_path)
        self.download_manager.show()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Modern Web Browser')
    
    window = Browser()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
