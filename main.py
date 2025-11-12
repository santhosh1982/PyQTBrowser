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
from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest, QWebEngineProfile, QWebEngineScript


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


class ThemeManager:
    def __init__(self):
        self.themes = {
            'Light': {
                'name': 'Light',
                'primary': '#4a90e2',
                'primary_hover': '#357abd',
                'primary_pressed': '#2868a8',
                'background': '#f5f5f5',
                'surface': '#ffffff',
                'border': '#e0e0e0',
                'text': '#333333',
                'text_secondary': '#666666',
                'danger': '#e74c3c',
                'danger_hover': '#c0392b',
                'success': '#27ae60',
                'success_hover': '#229954',
                'toolbar_gradient_start': '#ffffff',
                'toolbar_gradient_end': '#f0f0f0',
                'tab_gradient_start': '#f0f0f0',
                'tab_gradient_end': '#e0e0e0',
                'hover_bg': '#e8f4fd'
            },
            'Dark': {
                'name': 'Dark',
                'primary': '#5dade2',
                'primary_hover': '#3498db',
                'primary_pressed': '#2980b9',
                'background': '#1e1e1e',
                'surface': '#2d2d2d',
                'border': '#404040',
                'text': '#e0e0e0',
                'text_secondary': '#b0b0b0',
                'danger': '#e74c3c',
                'danger_hover': '#c0392b',
                'success': '#27ae60',
                'success_hover': '#229954',
                'toolbar_gradient_start': '#2d2d2d',
                'toolbar_gradient_end': '#252525',
                'tab_gradient_start': '#3a3a3a',
                'tab_gradient_end': '#2d2d2d',
                'hover_bg': '#3a4a5a'
            },
            'Ocean': {
                'name': 'Ocean',
                'primary': '#16a085',
                'primary_hover': '#138d75',
                'primary_pressed': '#117a65',
                'background': '#e8f8f5',
                'surface': '#ffffff',
                'border': '#a3e4d7',
                'text': '#1a5f5f',
                'text_secondary': '#45817e',
                'danger': '#e74c3c',
                'danger_hover': '#c0392b',
                'success': '#1abc9c',
                'success_hover': '#17a589',
                'toolbar_gradient_start': '#d5f4e6',
                'toolbar_gradient_end': '#c8ede0',
                'tab_gradient_start': '#c8ede0',
                'tab_gradient_end': '#b8e6d5',
                'hover_bg': '#d5f4e6'
            },
            'Sunset': {
                'name': 'Sunset',
                'primary': '#e67e22',
                'primary_hover': '#d35400',
                'primary_pressed': '#ba4a00',
                'background': '#fef5e7',
                'surface': '#ffffff',
                'border': '#f8c471',
                'text': '#7d3c00',
                'text_secondary': '#a04000',
                'danger': '#e74c3c',
                'danger_hover': '#c0392b',
                'success': '#27ae60',
                'success_hover': '#229954',
                'toolbar_gradient_start': '#fdebd0',
                'toolbar_gradient_end': '#fce5c3',
                'tab_gradient_start': '#fce5c3',
                'tab_gradient_end': '#faddb3',
                'hover_bg': '#ffe8cc'
            },
            'Forest': {
                'name': 'Forest',
                'primary': '#27ae60',
                'primary_hover': '#229954',
                'primary_pressed': '#1e8449',
                'background': '#e8f8f5',
                'surface': '#ffffff',
                'border': '#a9dfbf',
                'text': '#145a32',
                'text_secondary': '#1e8449',
                'danger': '#e74c3c',
                'danger_hover': '#c0392b',
                'success': '#27ae60',
                'success_hover': '#229954',
                'toolbar_gradient_start': '#d5f4e6',
                'toolbar_gradient_end': '#c8ede0',
                'tab_gradient_start': '#c8ede0',
                'tab_gradient_end': '#aed6a1',
                'hover_bg': '#d4edda'
            }
        }
    
    def get_theme(self, theme_name):
        return self.themes.get(theme_name, self.themes['Light'])
    
    def get_theme_names(self):
        return list(self.themes.keys())
    
    def generate_stylesheet(self, theme_name):
        theme = self.get_theme(theme_name)
        return f"""
            QMainWindow {{
                background-color: {theme['background']};
            }}
            QToolBar {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme['toolbar_gradient_start']}, stop:1 {theme['toolbar_gradient_end']});
                border: none;
                border-bottom: 1px solid {theme['border']};
                spacing: 8px;
                padding: 8px;
            }}
            QLineEdit {{
                border: 2px solid {theme['border']};
                border-radius: 20px;
                padding: 8px 16px;
                background-color: {theme['surface']};
                color: {theme['text']};
                font-size: 13px;
                selection-background-color: {theme['primary']};
            }}
            QLineEdit:focus {{
                border: 2px solid {theme['primary']};
                background-color: {theme['surface']};
            }}
            QPushButton {{
                background-color: {theme['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {theme['primary_hover']};
            }}
            QPushButton:pressed {{
                background-color: {theme['primary_pressed']};
            }}
            QTabWidget::pane {{
                border: none;
                background-color: {theme['surface']};
            }}
            QTabBar::tab {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme['tab_gradient_start']}, stop:1 {theme['tab_gradient_end']});
                border: 1px solid {theme['border']};
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 8px 16px;
                margin-right: 2px;
                min-width: 120px;
                color: {theme['text']};
            }}
            QTabBar::tab:selected {{
                background: {theme['surface']};
                border-bottom: 2px solid {theme['primary']};
            }}
            QTabBar::tab:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme['surface']}, stop:1 {theme['tab_gradient_start']});
            }}
            QMenuBar {{
                background-color: {theme['surface']};
                border-bottom: 1px solid {theme['border']};
                padding: 4px;
                color: {theme['text']};
            }}
            QMenuBar::item {{
                padding: 6px 12px;
                border-radius: 4px;
                color: {theme['text']};
            }}
            QMenuBar::item:selected {{
                background-color: {theme['primary']};
                color: white;
            }}
            QMenu {{
                background-color: {theme['surface']};
                border: 1px solid {theme['border']};
                border-radius: 6px;
                padding: 4px;
                color: {theme['text']};
            }}
            QMenu::item {{
                padding: 8px 24px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {theme['primary']};
                color: white;
            }}
            QToolBar QToolButton {{
                background-color: transparent;
                border: none;
                border-radius: 6px;
                padding: 6px;
                font-size: 18px;
                font-weight: bold;
                color: {theme['text']};
            }}
            QToolBar QToolButton:hover {{
                background-color: {theme['hover_bg']};
                color: {theme['primary']};
            }}
            QToolBar QToolButton:pressed {{
                background-color: {theme['border']};
            }}
        """


class ExtensionManager:
    def __init__(self):
        self.extensions_dir = 'browser_extensions'
        self.extensions_file = 'extensions.json'
        self.extensions = self.load_extensions()
        
        if not os.path.exists(self.extensions_dir):
            os.makedirs(self.extensions_dir)
    
    def load_extensions(self):
        if os.path.exists(self.extensions_file):
            with open(self.extensions_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_extensions(self):
        with open(self.extensions_file, 'w') as f:
            json.dump(self.extensions, f, indent=4)
    
    def add_extension(self, name, script_path, enabled=True):
        extension = {
            'id': len(self.extensions) + 1,
            'name': name,
            'script_path': script_path,
            'enabled': enabled
        }
        self.extensions.append(extension)
        self.save_extensions()
        return extension
    
    def remove_extension(self, extension_id):
        self.extensions = [ext for ext in self.extensions if ext['id'] != extension_id]
        self.save_extensions()
    
    def toggle_extension(self, extension_id):
        for ext in self.extensions:
            if ext['id'] == extension_id:
                ext['enabled'] = not ext['enabled']
                self.save_extensions()
                return ext['enabled']
        return False
    
    def get_enabled_extensions(self):
        return [ext for ext in self.extensions if ext['enabled']]


class SettingsManager:
    def __init__(self):
        self.settings_file = 'browser_settings.json'
        self.default_settings = {
            'homepage': 'https://www.google.com',
            'search_engine': 'https://www.google.com/search?q=',
            'download_path': os.path.expanduser('~/Downloads'),
            'theme': 'Light'
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


class SessionManager:
    def __init__(self):
        self.session_file = 'browser_session.json'
    
    def save_session(self, tabs_data, pinned_tabs):
        """Save current browser session"""
        session = {
            'tabs': tabs_data,
            'pinned_tabs': list(pinned_tabs)
        }
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session, f, indent=4)
        except Exception as e:
            print(f"Error saving session: {str(e)}")
    
    def load_session(self):
        """Load saved browser session"""
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading session: {str(e)}")
        return None
    
    def clear_session(self):
        """Clear saved session"""
        if os.path.exists(self.session_file):
            os.remove(self.session_file)


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
        self.setWindowTitle('📥 Download Manager')
        self.setGeometry(100, 100, 700, 500)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
                padding: 8px;
            }
            QListWidget {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px;
            }
            QProgressBar {
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                text-align: center;
                background-color: #f0f0f0;
                height: 24px;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a90e2, stop:1 #357abd);
                border-radius: 4px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel('📦 Active Downloads')
        layout.addWidget(title_label)
        
        self.download_list = QListWidget()
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
        self.setWindowTitle('⭐ Bookmarks')
        self.setGeometry(100, 100, 700, 500)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                padding: 8px;
            }
            QListWidget {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f0f0f0;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #e8f4fd;
            }
            QListWidget::item:selected {
                background-color: #4a90e2;
                color: white;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton#deleteBtn {
                background-color: #e74c3c;
            }
            QPushButton#deleteBtn:hover {
                background-color: #c0392b;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel('📚 Your Bookmarks')
        layout.addWidget(title_label)
        
        self.bookmark_list = QListWidget()
        self.bookmark_list.itemDoubleClicked.connect(self.open_bookmark)
        layout.addWidget(self.bookmark_list)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        delete_btn = QPushButton('🗑️ Delete Selected')
        delete_btn.setObjectName('deleteBtn')
        delete_btn.clicked.connect(self.delete_bookmark)
        button_layout.addWidget(delete_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton('✓ Close')
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
        self.setWindowTitle('📜 Browsing History')
        self.setGeometry(100, 100, 700, 500)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                padding: 8px;
            }
            QListWidget {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f0f0f0;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #e8f4fd;
            }
            QListWidget::item:selected {
                background-color: #4a90e2;
                color: white;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton#clearBtn {
                background-color: #e74c3c;
            }
            QPushButton#clearBtn:hover {
                background-color: #c0392b;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel('🕒 Your Browsing History')
        layout.addWidget(title_label)
        
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.open_history_item)
        layout.addWidget(self.history_list)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        clear_btn = QPushButton('🗑️ Clear All History')
        clear_btn.setObjectName('clearBtn')
        clear_btn.clicked.connect(self.clear_history)
        button_layout.addWidget(clear_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton('✓ Close')
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


class ThemeDialog(QDialog):
    def __init__(self, theme_manager, current_theme, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.current_theme = current_theme
        self.selected_theme = current_theme
        self.setWindowTitle('🎨 Browser Themes')
        self.setGeometry(100, 100, 600, 500)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
                padding: 8px;
            }
            QListWidget {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 16px;
                border-bottom: 1px solid #f0f0f0;
                border-radius: 6px;
                margin: 4px;
            }
            QListWidget::item:hover {
                background-color: #e8f4fd;
            }
            QListWidget::item:selected {
                background-color: #4a90e2;
                color: white;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton#applyBtn {
                background-color: #27ae60;
            }
            QPushButton#applyBtn:hover {
                background-color: #229954;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel('🎨 Choose Your Theme')
        layout.addWidget(title_label)
        
        desc_label = QLabel('Select a theme to customize your browser appearance')
        desc_label.setStyleSheet('font-size: 12px; font-weight: normal; color: #666666;')
        layout.addWidget(desc_label)
        
        self.theme_list = QListWidget()
        self.theme_list.itemClicked.connect(self.on_theme_selected)
        
        for theme_name in self.theme_manager.get_theme_names():
            item = QListWidgetItem(f"🎨 {theme_name}")
            item.setData(Qt.ItemDataRole.UserRole, theme_name)
            self.theme_list.addItem(item)
            if theme_name == current_theme:
                item.setSelected(True)
        
        layout.addWidget(self.theme_list)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        button_layout.addStretch()
        
        cancel_btn = QPushButton('✗ Cancel')
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        apply_btn = QPushButton('✓ Apply Theme')
        apply_btn.setObjectName('applyBtn')
        apply_btn.clicked.connect(self.apply_theme)
        button_layout.addWidget(apply_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def on_theme_selected(self, item):
        self.selected_theme = item.data(Qt.ItemDataRole.UserRole)
    
    def apply_theme(self):
        self.accept()
    
    def get_selected_theme(self):
        return self.selected_theme


class ExtensionDialog(QDialog):
    def __init__(self, extension_manager, parent=None):
        super().__init__(parent)
        self.extension_manager = extension_manager
        self.setWindowTitle('🧩 Extension Manager')
        self.setGeometry(100, 100, 700, 500)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
                padding: 8px;
            }
            QListWidget {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f0f0f0;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #e8f4fd;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton#addBtn {
                background-color: #27ae60;
            }
            QPushButton#addBtn:hover {
                background-color: #229954;
            }
            QPushButton#removeBtn {
                background-color: #e74c3c;
            }
            QPushButton#removeBtn:hover {
                background-color: #c0392b;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel('🧩 Manage Browser Extensions')
        layout.addWidget(title_label)
        
        desc_label = QLabel('Add custom JavaScript extensions to enhance your browsing experience')
        desc_label.setStyleSheet('font-size: 12px; font-weight: normal; color: #666666;')
        layout.addWidget(desc_label)
        
        self.extension_list = QListWidget()
        layout.addWidget(self.extension_list)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        add_btn = QPushButton('➕ Add Extension')
        add_btn.setObjectName('addBtn')
        add_btn.clicked.connect(self.add_extension)
        button_layout.addWidget(add_btn)
        
        toggle_btn = QPushButton('🔄 Toggle Enable/Disable')
        toggle_btn.clicked.connect(self.toggle_extension)
        button_layout.addWidget(toggle_btn)
        
        remove_btn = QPushButton('🗑️ Remove')
        remove_btn.setObjectName('removeBtn')
        remove_btn.clicked.connect(self.remove_extension)
        button_layout.addWidget(remove_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton('✓ Close')
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.load_extensions()
    
    def load_extensions(self):
        self.extension_list.clear()
        for ext in self.extension_manager.extensions:
            status = '✓ Enabled' if ext['enabled'] else '✗ Disabled'
            item = QListWidgetItem(f"{ext['name']} - {status}")
            item.setData(Qt.ItemDataRole.UserRole, ext)
            self.extension_list.addItem(item)
    
    def add_extension(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select Extension Script', '', 'JavaScript Files (*.js);;All Files (*.*)'
        )
        
        if file_path:
            name, ok = QInputDialog.getText(self, 'Extension Name', 'Enter extension name:')
            if ok and name:
                # Copy the file to extensions directory
                dest_path = os.path.join(self.extension_manager.extensions_dir, os.path.basename(file_path))
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as src:
                        content = src.read()
                    with open(dest_path, 'w', encoding='utf-8') as dst:
                        dst.write(content)
                    
                    self.extension_manager.add_extension(name, dest_path)
                    self.load_extensions()
                    QMessageBox.information(self, 'Success', f'Extension "{name}" added successfully!')
                    
                    if self.parent():
                        self.parent().load_extensions()
                except Exception as e:
                    QMessageBox.critical(self, 'Error', f'Failed to add extension: {str(e)}')
    
    def toggle_extension(self):
        current_item = self.extension_list.currentItem()
        if current_item:
            ext = current_item.data(Qt.ItemDataRole.UserRole)
            enabled = self.extension_manager.toggle_extension(ext['id'])
            self.load_extensions()
            status = 'enabled' if enabled else 'disabled'
            QMessageBox.information(self, 'Extension Toggled', f'Extension "{ext["name"]}" is now {status}!')
            
            if self.parent():
                self.parent().load_extensions()
    
    def remove_extension(self):
        current_item = self.extension_list.currentItem()
        if current_item:
            ext = current_item.data(Qt.ItemDataRole.UserRole)
            reply = QMessageBox.question(
                self, 'Remove Extension',
                f'Are you sure you want to remove "{ext["name"]}"?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.extension_manager.remove_extension(ext['id'])
                self.load_extensions()
                QMessageBox.information(self, 'Extension Removed', f'Extension "{ext["name"]}" has been removed!')
                
                if self.parent():
                    self.parent().load_extensions()


class SettingsDialog(QDialog):
    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.setWindowTitle('⚙️ Browser Settings')
        self.setGeometry(100, 100, 600, 400)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #333333;
                padding: 4px;
            }
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #4a90e2;
            }
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: #ffffff;
                font-size: 13px;
            }
            QComboBox:focus {
                border: 2px solid #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton#saveBtn {
                background-color: #27ae60;
            }
            QPushButton#saveBtn:hover {
                background-color: #229954;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
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
        button_layout.setSpacing(10)
        
        button_layout.addStretch()
        
        cancel_btn = QPushButton('✗ Cancel')
        cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton('💾 Save Settings')
        save_btn.setObjectName('saveBtn')
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
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
        self.session_manager = SessionManager()
        self.theme_manager = ThemeManager()
        self.extension_manager = ExtensionManager()
        self.download_manager = DownloadManager(self)
        
        self.setWindowTitle('Modern Web Browser')
        self.setGeometry(100, 100, 1200, 800)
        
        # Apply theme
        current_theme = self.settings_manager.get('theme')
        self.apply_theme(current_theme)
        
        # Old stylesheet - will be replaced by apply_theme
        old_stylesheet = """
            QMainWindow {
                background-color: #f5f5f5;
            }
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f0f0f0);
                border: none;
                border-bottom: 1px solid #d0d0d0;
                spacing: 8px;
                padding: 8px;
            }
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 20px;
                padding: 8px 16px;
                background-color: #ffffff;
                font-size: 13px;
                selection-background-color: #4a90e2;
            }
            QLineEdit:focus {
                border: 2px solid #4a90e2;
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2868a8;
            }
            QTabWidget::pane {
                border: none;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f0f0, stop:1 #e0e0e0);
                border: 1px solid #d0d0d0;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 8px 16px;
                margin-right: 2px;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                border-bottom: 2px solid #4a90e2;
            }
            QTabBar::tab:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f0f0f0);
            }
            QMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e0e0e0;
                padding: 4px;
            }
            QMenuBar::item {
                padding: 6px 12px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #4a90e2;
                color: white;
            }
            QMenu {
                background-color: #ffffff;
                border: 1px solid #d0d0d0;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 24px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #4a90e2;
                color: white;
            }
            QToolBar QToolButton {
                background-color: transparent;
                border: none;
                border-radius: 6px;
                padding: 6px;
                font-size: 18px;
                font-weight: bold;
                color: #333333;
            }
            QToolBar QToolButton:hover {
                background-color: #e8f4fd;
                color: #4a90e2;
            }
            QToolBar QToolButton:pressed {
                background-color: #d0e8f7;
            }
        """
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)
        
        # Tab pinning support
        self.pinned_tabs = set()  # Store indices of pinned tabs
        self.tabs.tabBar().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabs.tabBar().customContextMenuRequested.connect(self.show_tab_context_menu)
        
        self.setCentralWidget(self.tabs)
        
        navbar = QToolBar()
        navbar.setMovable(False)
        navbar.setIconSize(QSize(28, 28))
        self.addToolBar(navbar)
        
        back_btn = QAction('◀', self)
        back_btn.setToolTip('Back')
        back_btn.triggered.connect(lambda: self.current_browser().back())
        navbar.addAction(back_btn)
        
        forward_btn = QAction('▶', self)
        forward_btn.setToolTip('Forward')
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        navbar.addAction(forward_btn)
        
        reload_btn = QAction('↻', self)
        reload_btn.setToolTip('Reload')
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        navbar.addAction(reload_btn)
        
        home_btn = QAction('🏠', self)
        home_btn.setToolTip('Home')
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)
        
        navbar.addSeparator()
        
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText('🔍 Search or enter website address...')
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        
        navbar.addSeparator()
        
        new_tab_btn = QAction('➕', self)
        new_tab_btn.setToolTip('New Tab')
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(QUrl(self.settings_manager.get('homepage')), 'New Tab'))
        navbar.addAction(new_tab_btn)
        
        bookmark_add_btn = QAction('⭐', self)
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
        
        tools_menu.addSeparator()
        
        theme_action = QAction('🎨 Themes', self)
        theme_action.triggered.connect(self.show_themes)
        tools_menu.addAction(theme_action)
        
        extensions_action = QAction('🧩 Extensions', self)
        extensions_action.triggered.connect(self.show_extensions)
        tools_menu.addAction(extensions_action)
        
        tools_menu.addSeparator()
        
        settings_action = QAction('Settings', self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
        QWebEngineProfile.defaultProfile().downloadRequested.connect(self.on_download_requested)
        
        # Load extensions
        self.load_extensions()
        
        # Restore previous session or open homepage
        self.restore_session()
        
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
        # Don't close pinned tabs
        if i in self.pinned_tabs:
            QMessageBox.information(self, 'Pinned Tab', 'Cannot close a pinned tab. Unpin it first!')
            return
        
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)
            # Update pinned tabs indices after removal
            self.pinned_tabs = {idx if idx < i else idx - 1 for idx in self.pinned_tabs}
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
    
    def show_themes(self):
        current_theme = self.settings_manager.get('theme')
        dialog = ThemeDialog(self.theme_manager, current_theme, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_theme = dialog.get_selected_theme()
            self.settings_manager.set('theme', selected_theme)
            self.apply_theme(selected_theme)
            QMessageBox.information(self, 'Theme Applied', f'Theme "{selected_theme}" has been applied!')
    
    def show_extensions(self):
        dialog = ExtensionDialog(self.extension_manager, self)
        dialog.exec()
    
    def apply_theme(self, theme_name):
        stylesheet = self.theme_manager.generate_stylesheet(theme_name)
        self.setStyleSheet(stylesheet)
    
    def load_extensions(self):
        profile = QWebEngineProfile.defaultProfile()
        scripts = profile.scripts()
        
        # Clear existing custom scripts
        scripts.clear()
        
        # Load enabled extensions
        for ext in self.extension_manager.get_enabled_extensions():
            try:
                if os.path.exists(ext['script_path']):
                    with open(ext['script_path'], 'r', encoding='utf-8') as f:
                        script_source = f.read()
                    
                    script = QWebEngineScript()
                    script.setName(ext['name'])
                    script.setSourceCode(script_source)
                    script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentReady)
                    script.setRunsOnSubFrames(True)
                    script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
                    
                    scripts.insert(script)
            except Exception as e:
                print(f"Error loading extension {ext['name']}: {str(e)}")
    
    def show_tab_context_menu(self, position):
        """Show context menu for tab operations"""
        tab_bar = self.tabs.tabBar()
        tab_index = tab_bar.tabAt(position)
        
        if tab_index < 0:
            return
        
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                padding: 8px;
            }
            QMenu::item {
                padding: 8px 24px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #4a90e2;
                color: white;
            }
        """)
        
        # Pin/Unpin action
        is_pinned = tab_index in self.pinned_tabs
        pin_text = '📌 Unpin Tab' if is_pinned else '📍 Pin Tab'
        pin_action = menu.addAction(pin_text)
        pin_action.triggered.connect(lambda: self.toggle_pin_tab(tab_index))
        
        menu.addSeparator()
        
        # Duplicate tab
        duplicate_action = menu.addAction('📋 Duplicate Tab')
        duplicate_action.triggered.connect(lambda: self.duplicate_tab(tab_index))
        
        # Reload tab
        reload_action = menu.addAction('↻ Reload Tab')
        reload_action.triggered.connect(lambda: self.reload_tab(tab_index))
        
        menu.addSeparator()
        
        # Close tab
        close_action = menu.addAction('✗ Close Tab')
        close_action.triggered.connect(lambda: self.close_tab(tab_index))
        
        # Close other tabs
        close_others_action = menu.addAction('✗ Close Other Tabs')
        close_others_action.triggered.connect(lambda: self.close_other_tabs(tab_index))
        
        # Close tabs to the right
        close_right_action = menu.addAction('✗ Close Tabs to the Right')
        close_right_action.triggered.connect(lambda: self.close_tabs_to_right(tab_index))
        
        menu.exec(tab_bar.mapToGlobal(position))
    
    def toggle_pin_tab(self, tab_index):
        """Pin or unpin a tab"""
        if tab_index in self.pinned_tabs:
            # Unpin the tab
            self.pinned_tabs.remove(tab_index)
            self.tabs.setTabText(tab_index, self.tabs.tabText(tab_index).replace('📌 ', ''))
            self.tabs.tabBar().setTabButton(tab_index, self.tabs.tabBar().ButtonPosition.RightSide, 
                                           self.tabs.tabBar().tabButton(tab_index, self.tabs.tabBar().ButtonPosition.RightSide))
        else:
            # Pin the tab
            self.pinned_tabs.add(tab_index)
            current_text = self.tabs.tabText(tab_index)
            if not current_text.startswith('📌 '):
                self.tabs.setTabText(tab_index, f'📌 {current_text}')
            # Hide close button for pinned tabs
            self.tabs.tabBar().setTabButton(tab_index, self.tabs.tabBar().ButtonPosition.RightSide, None)
    
    def duplicate_tab(self, tab_index):
        """Duplicate a tab"""
        browser = self.tabs.widget(tab_index)
        if browser:
            url = browser.url()
            self.add_new_tab(url, f'Copy of {self.tabs.tabText(tab_index)}')
    
    def reload_tab(self, tab_index):
        """Reload a specific tab"""
        browser = self.tabs.widget(tab_index)
        if browser:
            browser.reload()
    
    def close_other_tabs(self, tab_index):
        """Close all tabs except the specified one"""
        # Close tabs from right to left to maintain indices
        for i in range(self.tabs.count() - 1, -1, -1):
            if i != tab_index and i not in self.pinned_tabs:
                self.tabs.removeTab(i)
    
    def close_tabs_to_right(self, tab_index):
        """Close all tabs to the right of the specified tab"""
        for i in range(self.tabs.count() - 1, tab_index, -1):
            if i not in self.pinned_tabs:
                self.tabs.removeTab(i)
    
    def save_session(self):
        """Save current browser session"""
        tabs_data = []
        for i in range(self.tabs.count()):
            browser = self.tabs.widget(i)
            if browser:
                url = browser.url().toString()
                title = self.tabs.tabText(i).replace('📌 ', '')  # Remove pin icon from title
                tabs_data.append({
                    'url': url,
                    'title': title,
                    'index': i
                })
        
        self.session_manager.save_session(tabs_data, self.pinned_tabs)
    
    def restore_session(self):
        """Restore previous browser session"""
        session = self.session_manager.load_session()
        
        if session and session.get('tabs'):
            # Restore tabs
            for tab_data in session['tabs']:
                url = tab_data.get('url', self.settings_manager.get('homepage'))
                title = tab_data.get('title', 'New Tab')
                
                # Skip about:blank or empty URLs
                if url and url != 'about:blank':
                    self.add_new_tab(QUrl(url), title)
            
            # Restore pinned tabs
            pinned_indices = session.get('pinned_tabs', [])
            for idx in pinned_indices:
                if idx < self.tabs.count():
                    self.toggle_pin_tab(idx)
        else:
            # No session found, open homepage
            self.add_new_tab(QUrl(self.settings_manager.get('homepage')), 'Home')
    
    def closeEvent(self, event):
        """Save session before closing"""
        self.save_session()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Modern Web Browser')
    
    window = Browser()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
