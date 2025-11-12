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
                              QProgressBar, QListWidgetItem, QComboBox, QSplitter,
                              QTextEdit, QScrollArea, QFrame)
from PyQt6.QtGui import QIcon, QAction, QKeySequence, QTextCursor
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import (QWebEngineDownloadRequest, QWebEngineProfile, 
                                   QWebEngineScript, QWebEnginePage)


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
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def createWindow(self, window_type):
        new_tab = self.parent_browser.add_new_tab(QUrl('about:blank'), 'New Tab')
        return new_tab
    
    def show_context_menu(self, position):
        """Show custom context menu with AI actions"""
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
            QMenu::separator {
                height: 1px;
                background: #e0e0e0;
                margin: 4px 0;
            }
        """)
        
        # Get selected text
        self.page().runJavaScript("window.getSelection().toString();", 
                                  lambda text: self.build_context_menu(menu, text, position))
    
    def build_context_menu(self, menu, selected_text, position):
        """Build context menu based on selected text"""
        has_selection = selected_text and selected_text.strip()
        
        if has_selection:
            # AI Actions for selected text
            ai_menu = menu.addMenu("🤖 Ask AI")
            ai_menu.setStyleSheet(menu.styleSheet())
            
            explain_action = ai_menu.addAction("💡 Explain this")
            explain_action.triggered.connect(lambda: self.send_to_ai("explain", selected_text))
            
            summarize_action = ai_menu.addAction("📄 Summarize this")
            summarize_action.triggered.connect(lambda: self.send_to_ai("summarize", selected_text))
            
            translate_action = ai_menu.addAction("🌐 Translate this")
            translate_action.triggered.connect(lambda: self.send_to_ai("translate", selected_text))
            
            simplify_action = ai_menu.addAction("📝 Simplify this")
            simplify_action.triggered.connect(lambda: self.send_to_ai("simplify", selected_text))
            
            define_action = ai_menu.addAction("📖 Define terms")
            define_action.triggered.connect(lambda: self.send_to_ai("define", selected_text))
            
            ai_menu.addSeparator()
            
            ask_action = ai_menu.addAction("💬 Ask about this...")
            ask_action.triggered.connect(lambda: self.send_to_ai("ask", selected_text))
            
            menu.addSeparator()
        
        # Standard browser actions
        back_action = menu.addAction("◀ Back")
        back_action.triggered.connect(self.back)
        back_action.setEnabled(self.history().canGoBack())
        
        forward_action = menu.addAction("▶ Forward")
        forward_action.triggered.connect(self.forward)
        forward_action.setEnabled(self.history().canGoForward())
        
        reload_action = menu.addAction("↻ Reload")
        reload_action.triggered.connect(self.reload)
        
        menu.addSeparator()
        
        # Developer Tools
        inspect_action = menu.addAction("🔍 Inspect Element")
        inspect_action.triggered.connect(lambda: self.inspect_element_at_position(position))
        
        view_source_action = menu.addAction("📄 View Page Source")
        view_source_action.triggered.connect(self.view_page_source)
        
        menu.addSeparator()
        
        if has_selection:
            copy_action = menu.addAction("📋 Copy")
            copy_action.triggered.connect(lambda: self.page().triggerAction(self.page().WebAction.Copy))
            
            search_action = menu.addAction("🔍 Search with Google")
            search_action.triggered.connect(lambda: self.search_selected(selected_text))
        
        # Show menu at cursor position
        menu.exec(self.mapToGlobal(position))
    
    def send_to_ai(self, action, text):
        """Send selected text to AI chat with specific action"""
        if not self.parent_browser:
            return
        
        # Open AI panel if not visible
        if not self.parent_browser.ai_panel_visible:
            self.parent_browser.toggle_ai_panel()
        
        # Get AI panel
        ai_panel = self.parent_browser.ai_panel
        
        # Prepare prompt based on action
        prompts = {
            "explain": f"Please explain the following text in detail:\n\n{text}",
            "summarize": f"Please provide a concise summary of:\n\n{text}",
            "translate": f"Please translate the following text to English (or if already in English, translate to Spanish):\n\n{text}",
            "simplify": f"Please simplify and explain in simple terms:\n\n{text}",
            "define": f"Please define and explain the key terms in:\n\n{text}",
            "ask": text  # For custom questions, just use the text as context
        }
        
        prompt = prompts.get(action, text)
        
        # Send directly to AI with selection indicator
        ai_panel.add_user_message(prompt, from_selection=True)
        response = ai_panel.generate_ai_response(prompt)
        ai_panel.add_ai_message(response)
    
    def search_selected(self, text):
        """Search selected text with Google"""
        if self.parent_browser:
            search_url = f"https://www.google.com/search?q={text.replace(' ', '+')}"
            self.parent_browser.add_new_tab(QUrl(search_url), f"Search: {text[:20]}...")
    
    def inspect_element_at_position(self, position):
        """Inspect element at cursor position"""
        if not self.parent_browser:
            return
        
        # Open DevTools if not visible
        if not self.parent_browser.devtools_visible:
            self.parent_browser.toggle_devtools()
        
        # Switch to Elements tab
        self.parent_browser.devtools_panel.tools_tabs.setCurrentIndex(2)  # Elements tab
        
        # Get element at position using JavaScript
        script = f"""
        (function() {{
            var element = document.elementFromPoint({position.x()}, {position.y()});
            if (element) {{
                var html = element.outerHTML;
                var tagName = element.tagName.toLowerCase();
                var id = element.id ? '#' + element.id : '';
                var classes = element.className ? '.' + element.className.split(' ').join('.') : '';
                var selector = tagName + id + classes;
                
                return {{
                    html: html,
                    selector: selector,
                    tagName: tagName,
                    id: element.id,
                    className: element.className,
                    textContent: element.textContent.substring(0, 100)
                }};
            }}
            return null;
        }})();
        """
        
        self.page().runJavaScript(script, lambda result: self.display_inspected_element(result))
    
    def display_inspected_element(self, element_info):
        """Display inspected element in DevTools"""
        if not element_info or not self.parent_browser:
            return
        
        devtools = self.parent_browser.devtools_panel
        
        # Format element information
        output = f"""🔍 INSPECTED ELEMENT
{'=' * 50}

Selector: {element_info.get('selector', 'N/A')}
Tag: <{element_info.get('tagName', 'N/A')}>
ID: {element_info.get('id', '(none)')}
Class: {element_info.get('className', '(none)')}

HTML:
{'-' * 50}
{element_info.get('html', 'N/A')}

Text Content:
{'-' * 50}
{element_info.get('textContent', 'N/A')}
"""
        
        devtools.elements_display.setPlainText(output)
        devtools.log_console(f"Inspected: {element_info.get('selector', 'element')}", "info")
    
    def view_page_source(self):
        """View page source in DevTools"""
        if not self.parent_browser:
            return
        
        # Open DevTools if not visible
        if not self.parent_browser.devtools_visible:
            self.parent_browser.toggle_devtools()
        
        # Switch to Elements tab
        self.parent_browser.devtools_panel.tools_tabs.setCurrentIndex(2)  # Elements tab
        
        # Get full page source
        script = "document.documentElement.outerHTML;"
        self.page().runJavaScript(script, lambda html: self.display_page_source(html))
    
    def display_page_source(self, html):
        """Display page source in DevTools"""
        if not html or not self.parent_browser:
            return
        
        devtools = self.parent_browser.devtools_panel
        
        # Format and display
        output = f"""📄 PAGE SOURCE
{'=' * 50}

{html}
"""
        
        devtools.elements_display.setPlainText(output)
        devtools.log_console("Viewing page source", "info")


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


class AIChatPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_browser = parent
        self.chat_history = []
        self.conversation_messages = []  # For AI context
        
        # Import AI providers
        try:
            from ai_providers import AIProviderManager, OpenAIProvider, GeminiProvider, ClaudeProvider
            self.provider_manager = AIProviderManager()
            self.providers = {
                'openai': OpenAIProvider,
                'gemini': GeminiProvider,
                'claude': ClaudeProvider
            }
            self.ai_enabled = True
        except Exception as e:
            print(f"AI providers not available: {e}")
            self.ai_enabled = False
            self.provider_manager = None
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a90e2, stop:1 #357abd);
                padding: 12px;
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QComboBox {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QComboBox:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #333;
                selection-background-color: #4a90e2;
            }
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(8, 8, 8, 8)
        
        title = QLabel("🤖 AI Chat")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Provider selector
        if self.ai_enabled and self.provider_manager:
            self.provider_combo = QComboBox()
            self.provider_combo.addItem("🔵 OpenAI", "openai")
            self.provider_combo.addItem("🟢 Gemini", "gemini")
            self.provider_combo.addItem("🟣 Claude", "claude")
            
            current_provider = self.provider_manager.get_selected_provider()
            index = self.provider_combo.findData(current_provider)
            if index >= 0:
                self.provider_combo.setCurrentIndex(index)
            
            self.provider_combo.currentIndexChanged.connect(self.on_provider_changed)
            header_layout.addWidget(self.provider_combo)
        
        settings_btn = QPushButton("⚙️")
        settings_btn.setToolTip("AI Settings")
        settings_btn.clicked.connect(self.show_settings)
        header_layout.addWidget(settings_btn)
        
        clear_btn = QPushButton("🗑️")
        clear_btn.setToolTip("Clear Chat")
        clear_btn.clicked.connect(self.clear_chat)
        header_layout.addWidget(clear_btn)
        
        layout.addWidget(header)
        
        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: none;
                padding: 12px;
                font-size: 15px;
                line-height: 1.8;
            }
        """)
        layout.addWidget(self.chat_display, 1)
        
        # Input area
        input_container = QWidget()
        input_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-top: 1px solid #e0e0e0;
                padding: 12px;
            }
        """)
        
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(8, 8, 8, 8)
        input_layout.setSpacing(8)
        
        # Quick actions
        actions_layout = QHBoxLayout()
        
        summarize_btn = QPushButton("📄 Summarize Page")
        summarize_btn.clicked.connect(self.summarize_page)
        actions_layout.addWidget(summarize_btn)
        
        explain_btn = QPushButton("💡 Explain")
        explain_btn.clicked.connect(self.explain_page)
        actions_layout.addWidget(explain_btn)
        
        input_layout.addLayout(actions_layout)
        
        # Message input
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Ask me anything about this page or general questions...")
        self.message_input.setMaximumHeight(80)
        self.message_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
                background-color: #ffffff;
            }
            QTextEdit:focus {
                border: 2px solid #4a90e2;
            }
        """)
        input_layout.addWidget(self.message_input)
        
        # Send button
        send_btn = QPushButton("📤 Send Message")
        send_btn.setStyleSheet("""
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
            QPushButton:pressed {
                background-color: #2868a8;
            }
        """)
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(send_btn)
        
        layout.addWidget(input_container)
        
        self.setLayout(layout)
        
        # Welcome message
        self.add_ai_message("👋 Hello! I'm your AI assistant. I can help you with:\n\n"
                           "• Summarizing web pages\n"
                           "• Explaining content\n"
                           "• Answering questions\n"
                           "• General assistance\n\n"
                           "Try the quick action buttons or type your question!")
    
    def add_user_message(self, message, from_selection=False):
        """Add user message to chat"""
        self.chat_history.append(('user', message))
        
        # Add indicator if from text selection
        indicator = "📌 " if from_selection else ""
        
        # Escape HTML and preserve line breaks
        message_html = message.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
        
        html = f"""
        <div style='margin: 10px 0; text-align: right;'>
            <div style='display: inline-block; background-color: #4a90e2; color: white; 
                        padding: 10px 15px; border-radius: 12px; max-width: 80%; text-align: left;'>
                <strong>{indicator}You:</strong><br>{message_html}
            </div>
        </div>
        """
        self.chat_display.append(html)
        self.chat_display.moveCursor(QTextCursor.MoveOperation.End)
    
    def add_ai_message(self, message):
        """Add AI message to chat"""
        self.chat_history.append(('ai', message))
        html = f"""
        <div style='margin: 10px 0;'>
            <div style='display: inline-block; background-color: #e8f4fd; color: #333; 
                        padding: 10px 15px; border-radius: 12px; max-width: 80%;'>
                <strong>🤖 AI:</strong><br>{message}
            </div>
        </div>
        """
        self.chat_display.append(html)
        self.chat_display.moveCursor(QTextCursor.MoveOperation.End)
    
    def send_message(self):
        """Send user message and get AI response"""
        message = self.message_input.toPlainText().strip()
        if not message:
            return
        
        self.add_user_message(message)
        self.message_input.clear()
        
        # Simulate AI response (in real implementation, call actual AI API)
        response = self.generate_ai_response(message)
        self.add_ai_message(response)
    
    def generate_ai_response(self, message, context=None):
        """Generate AI response using selected provider"""
        if not self.ai_enabled or not self.provider_manager:
            return ("💡 AI providers not configured. Please:\n\n"
                   "1. Install required libraries:\n"
                   "   pip install openai google-generativeai anthropic\n"
                   "2. Configure API keys in settings (⚙️ button)\n"
                   "3. Select your preferred provider")
        
        try:
            # Get selected provider
            provider_name = self.provider_manager.get_selected_provider()
            api_key = self.provider_manager.get_api_key(provider_name)
            model = self.provider_manager.get_model(provider_name)
            
            if not api_key:
                return (f"⚠️ {provider_name.upper()} API key not configured.\n\n"
                       f"Please click the ⚙️ Settings button to add your API key.")
            
            # Build conversation messages
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant integrated into a web browser. "
                                             "You can help users understand web content, answer questions, "
                                             "and provide information. Be concise and helpful."}
            ]
            
            # Add conversation history
            messages.extend(self.conversation_messages)
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Add context if provided
            if context:
                messages[-1]["content"] = f"Context: {context}\n\nQuestion: {message}"
            
            # Get provider instance
            provider_class = self.providers.get(provider_name)
            if not provider_class:
                return f"Error: Provider {provider_name} not found"
            
            provider = provider_class(api_key)
            
            # Generate response
            response = provider.generate_response(
                messages,
                model=model,
                temperature=self.provider_manager.config['settings']['temperature'],
                max_tokens=self.provider_manager.config['settings']['max_tokens']
            )
            
            # Update conversation history
            self.conversation_messages.append({"role": "user", "content": message})
            self.conversation_messages.append({"role": "assistant", "content": response})
            
            # Keep only last 10 messages for context
            if len(self.conversation_messages) > 20:
                self.conversation_messages = self.conversation_messages[-20:]
            
            return response
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def summarize_page(self):
        """Summarize current page"""
        self.add_user_message("📄 Summarize this page")
        self.add_ai_message("⏳ Extracting page content...")
        
        def handle_content(content):
            if content:
                prompt = f"Please provide a concise summary of this web page content:\n\n{content}"
                response = self.generate_ai_response(prompt)
                # Remove the loading message
                self.chat_history.pop()
                self.chat_display.clear()
                for role, msg in self.chat_history:
                    if role == 'user':
                        self.add_user_message(msg)
                    else:
                        self.add_ai_message(msg)
                self.add_ai_message(f"📄 **Summary:**\n\n{response}")
            else:
                self.add_ai_message("⚠️ Could not extract page content.")
        
        self.extract_page_content(handle_content)
    
    def explain_page(self):
        """Explain current page"""
        self.add_user_message("💡 Explain this page")
        self.add_ai_message("⏳ Analyzing page content...")
        
        def handle_content(content):
            if content:
                prompt = f"Please explain what this web page is about in detail, including main topics and key concepts:\n\n{content}"
                response = self.generate_ai_response(prompt)
                # Remove the loading message
                self.chat_history.pop()
                self.chat_display.clear()
                for role, msg in self.chat_history:
                    if role == 'user':
                        self.add_user_message(msg)
                    else:
                        self.add_ai_message(msg)
                self.add_ai_message(f"💡 **Explanation:**\n\n{response}")
            else:
                self.add_ai_message("⚠️ Could not extract page content.")
        
        self.extract_page_content(handle_content)
    
    def clear_chat(self):
        """Clear chat history"""
        self.chat_history.clear()
        self.conversation_messages.clear()
        self.chat_display.clear()
        self.add_ai_message("Chat cleared! How can I help you?")
    
    def on_provider_changed(self):
        """Handle provider selection change"""
        if self.ai_enabled and self.provider_manager:
            provider = self.provider_combo.currentData()
            self.provider_manager.set_selected_provider(provider)
            self.add_ai_message(f"Switched to {provider.upper()}. Ready to chat!")
    
    def show_settings(self):
        """Show AI settings dialog"""
        dialog = AISettingsDialog(self.provider_manager, self)
        dialog.exec()
    
    def extract_page_content(self, callback):
        """Extract text content from current page"""
        if self.parent_browser:
            browser = self.parent_browser.current_browser()
            if browser:
                script = """
                (function() {
                    // Get main content, excluding scripts, styles, etc.
                    let content = document.body.innerText;
                    // Limit to first 5000 characters
                    return content.substring(0, 5000);
                })();
                """
                browser.page().runJavaScript(script, callback)


class AISettingsDialog(QDialog):
    """Dialog for configuring AI settings"""
    
    def __init__(self, provider_manager, parent=None):
        super().__init__(parent)
        self.provider_manager = provider_manager
        self.setWindowTitle('⚙️ AI Settings')
        self.setGeometry(100, 100, 600, 500)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                font-size: 13px;
                color: #333333;
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
        
        # Title
        title = QLabel("🤖 AI Provider Configuration")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # OpenAI settings
        openai_group = QLabel("🔵 OpenAI (GPT)")
        openai_group.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(openai_group)
        
        self.openai_key = QLineEdit()
        self.openai_key.setPlaceholderText("Enter OpenAI API key (sk-...)")
        self.openai_key.setText(self.provider_manager.get_api_key('openai'))
        self.openai_key.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.openai_key)
        
        self.openai_model = QComboBox()
        self.openai_model.addItems(['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo-preview'])
        self.openai_model.setCurrentText(self.provider_manager.get_model('openai'))
        layout.addWidget(self.openai_model)
        
        # Gemini settings
        gemini_group = QLabel("🟢 Google Gemini")
        gemini_group.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(gemini_group)
        
        self.gemini_key = QLineEdit()
        self.gemini_key.setPlaceholderText("Enter Gemini API key")
        self.gemini_key.setText(self.provider_manager.get_api_key('gemini'))
        self.gemini_key.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.gemini_key)
        
        self.gemini_model = QComboBox()
        self.gemini_model.addItems(['gemini-pro', 'gemini-pro-vision'])
        self.gemini_model.setCurrentText(self.provider_manager.get_model('gemini'))
        layout.addWidget(self.gemini_model)
        
        # Claude settings
        claude_group = QLabel("🟣 Anthropic Claude")
        claude_group.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(claude_group)
        
        self.claude_key = QLineEdit()
        self.claude_key.setPlaceholderText("Enter Claude API key")
        self.claude_key.setText(self.provider_manager.get_api_key('claude'))
        self.claude_key.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.claude_key)
        
        self.claude_model = QComboBox()
        self.claude_model.addItems([
            'claude-3-opus-20240229',
            'claude-3-sonnet-20240229',
            'claude-3-haiku-20240307'
        ])
        self.claude_model.setCurrentText(self.provider_manager.get_model('claude'))
        layout.addWidget(self.claude_model)
        
        # Help text
        help_text = QLabel(
            "💡 Get API keys:\n"
            "• OpenAI: https://platform.openai.com/api-keys\n"
            "• Gemini: https://makersuite.google.com/app/apikey\n"
            "• Claude: https://console.anthropic.com/\n\n"
            "Install libraries: pip install openai google-generativeai anthropic"
        )
        help_text.setStyleSheet("font-size: 11px; color: #666; background: #fff; padding: 10px; border-radius: 6px;")
        help_text.setWordWrap(True)
        layout.addWidget(help_text)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("✗ Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("💾 Save Settings")
        save_btn.setObjectName('saveBtn')
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def save_settings(self):
        """Save AI settings"""
        # Save API keys
        self.provider_manager.set_api_key('openai', self.openai_key.text())
        self.provider_manager.set_api_key('gemini', self.gemini_key.text())
        self.provider_manager.set_api_key('claude', self.claude_key.text())
        
        # Save models
        self.provider_manager.set_model('openai', self.openai_model.currentText())
        self.provider_manager.set_model('gemini', self.gemini_model.currentText())
        self.provider_manager.set_model('claude', self.claude_model.currentText())
        
        QMessageBox.information(self, 'Settings Saved', 'AI settings have been saved successfully!')
        self.accept()


class DevToolsPanel(QWidget):
    """Developer Tools Panel with Console, Network, Elements, etc."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_browser = parent
        self.console_messages = []
        self.network_requests = []
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2c3e50, stop:1 #34495e);
                padding: 8px;
            }
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(8, 4, 8, 4)
        
        title = QLabel("🔧 Developer Tools")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.clicked.connect(self.clear_console)
        header_layout.addWidget(clear_btn)
        
        layout.addWidget(header)
        
        # Tab widget for different tools
        self.tools_tabs = QTabWidget()
        self.tools_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                background: #2d2d2d;
                color: #cccccc;
                padding: 8px 16px;
                border: none;
                border-right: 1px solid #1e1e1e;
            }
            QTabBar::tab:selected {
                background: #1e1e1e;
                color: #4a90e2;
                border-bottom: 2px solid #4a90e2;
            }
            QTabBar::tab:hover {
                background: #3d3d3d;
            }
        """)
        
        # Console Tab
        self.console_widget = self.create_console_tab()
        self.tools_tabs.addTab(self.console_widget, "📟 Console")
        
        # Network Tab
        self.network_widget = self.create_network_tab()
        self.tools_tabs.addTab(self.network_widget, "🌐 Network")
        
        # Elements Tab
        self.elements_widget = self.create_elements_tab()
        self.tools_tabs.addTab(self.elements_widget, "🔍 Elements")
        
        # Storage Tab
        self.storage_widget = self.create_storage_tab()
        self.tools_tabs.addTab(self.storage_widget, "💾 Storage")
        
        # Performance Tab
        self.performance_widget = self.create_performance_tab()
        self.tools_tabs.addTab(self.performance_widget, "⚡ Performance")
        
        layout.addWidget(self.tools_tabs)
        self.setLayout(layout)
    
    def create_console_tab(self):
        """Create console tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Console output
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #cccccc;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
                border: none;
                padding: 8px;
            }
        """)
        layout.addWidget(self.console_output)
        
        # Console input
        input_container = QWidget()
        input_container.setStyleSheet("background-color: #2d2d2d; padding: 8px;")
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(8, 4, 8, 4)
        
        prompt_label = QLabel("❯")
        prompt_label.setStyleSheet("color: #4a90e2; font-weight: bold; font-size: 14px;")
        input_layout.addWidget(prompt_label)
        
        self.console_input = QLineEdit()
        self.console_input.setPlaceholderText("Execute JavaScript...")
        self.console_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                color: #cccccc;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4a90e2;
            }
        """)
        self.console_input.returnPressed.connect(self.execute_console_command)
        input_layout.addWidget(self.console_input)
        
        layout.addWidget(input_container)
        
        # Add welcome message
        self.log_console("🔧 Developer Console Ready", "info")
        self.log_console("Type JavaScript commands to execute", "info")
        
        return widget
    
    def create_network_tab(self):
        """Create network monitoring tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Network list
        self.network_list = QListWidget()
        self.network_list.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                color: #cccccc;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #2d2d2d;
            }
            QListWidget::item:hover {
                background-color: #2d2d2d;
            }
            QListWidget::item:selected {
                background-color: #3d3d3d;
            }
        """)
        layout.addWidget(self.network_list)
        
        # Info label
        info_label = QLabel("🌐 Network requests will appear here when pages load")
        info_label.setStyleSheet("color: #888; font-size: 11px; padding: 8px;")
        layout.addWidget(info_label)
        
        return widget
    
    def create_elements_tab(self):
        """Create elements inspector tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Toolbar
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 8)
        
        inspect_btn = QPushButton("🔍 Inspect Element")
        inspect_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        inspect_btn.clicked.connect(self.inspect_element)
        toolbar_layout.addWidget(inspect_btn)
        
        toolbar_layout.addStretch()
        layout.addWidget(toolbar)
        
        # Elements tree
        self.elements_display = QTextEdit()
        self.elements_display.setReadOnly(True)
        self.elements_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #cccccc;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.elements_display)
        
        self.elements_display.setPlainText("Click 'Inspect Element' to view page structure")
        
        return widget
    
    def create_storage_tab(self):
        """Create storage inspector tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Storage info
        self.storage_display = QTextEdit()
        self.storage_display.setReadOnly(True)
        self.storage_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #cccccc;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.storage_display)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        cookies_btn = QPushButton("🍪 View Cookies")
        cookies_btn.clicked.connect(self.view_cookies)
        btn_layout.addWidget(cookies_btn)
        
        localstorage_btn = QPushButton("💾 View LocalStorage")
        localstorage_btn.clicked.connect(self.view_localstorage)
        btn_layout.addWidget(localstorage_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.storage_display.setPlainText("💾 Storage Inspector\n\nClick buttons above to view cookies and localStorage")
        
        return widget
    
    def create_performance_tab(self):
        """Create performance monitoring tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Performance metrics
        self.performance_display = QTextEdit()
        self.performance_display.setReadOnly(True)
        self.performance_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #cccccc;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.performance_display)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        measure_btn = QPushButton("⚡ Measure Performance")
        measure_btn.clicked.connect(self.measure_performance)
        btn_layout.addWidget(measure_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.performance_display.setPlainText("⚡ Performance Monitor\n\nClick 'Measure Performance' to analyze page metrics")
        
        return widget
    
    def log_console(self, message, level="log"):
        """Add message to console"""
        colors = {
            "log": "#cccccc",
            "info": "#4a90e2",
            "warn": "#f39c12",
            "error": "#e74c3c",
            "success": "#27ae60"
        }
        
        icons = {
            "log": "▸",
            "info": "ℹ",
            "warn": "⚠",
            "error": "✖",
            "success": "✓"
        }
        
        color = colors.get(level, "#cccccc")
        icon = icons.get(level, "▸")
        
        html = f'<span style="color: {color};">{icon} {message}</span><br>'
        self.console_output.append(html)
        self.console_messages.append((level, message))
    
    def execute_console_command(self):
        """Execute JavaScript command in console"""
        command = self.console_input.text().strip()
        if not command:
            return
        
        self.log_console(f"❯ {command}", "log")
        self.console_input.clear()
        
        if self.parent_browser:
            browser = self.parent_browser.current_browser()
            if browser:
                browser.page().runJavaScript(command, lambda result: self.handle_console_result(result))
    
    def handle_console_result(self, result):
        """Handle JavaScript execution result"""
        if result is not None:
            self.log_console(f"← {result}", "success")
        else:
            self.log_console("← undefined", "info")
    
    def clear_console(self):
        """Clear console output"""
        self.console_output.clear()
        self.console_messages.clear()
        self.log_console("Console cleared", "info")
    
    def inspect_element(self):
        """Inspect page elements"""
        if self.parent_browser:
            browser = self.parent_browser.current_browser()
            if browser:
                script = """
                (function() {
                    return document.documentElement.outerHTML;
                })();
                """
                browser.page().runJavaScript(script, self.display_elements)
    
    def display_elements(self, html):
        """Display page HTML structure"""
        if html:
            # Format HTML for display (simplified)
            formatted = html[:5000]  # Limit to first 5000 chars
            if len(html) > 5000:
                formatted += "\n\n... (truncated)"
            self.elements_display.setPlainText(formatted)
        else:
            self.elements_display.setPlainText("No HTML content available")
    
    def view_cookies(self):
        """View page cookies"""
        if self.parent_browser:
            browser = self.parent_browser.current_browser()
            if browser:
                script = "document.cookie;"
                browser.page().runJavaScript(script, lambda cookies: self.display_storage("Cookies", cookies))
    
    def view_localstorage(self):
        """View localStorage"""
        if self.parent_browser:
            browser = self.parent_browser.current_browser()
            if browser:
                script = """
                (function() {
                    let items = {};
                    for (let i = 0; i < localStorage.length; i++) {
                        let key = localStorage.key(i);
                        items[key] = localStorage.getItem(key);
                    }
                    return JSON.stringify(items, null, 2);
                })();
                """
                browser.page().runJavaScript(script, lambda storage: self.display_storage("LocalStorage", storage))
    
    def display_storage(self, storage_type, data):
        """Display storage data"""
        if data:
            self.storage_display.setPlainText(f"{storage_type}:\n\n{data}")
        else:
            self.storage_display.setPlainText(f"{storage_type}: Empty")
    
    def measure_performance(self):
        """Measure page performance"""
        if self.parent_browser:
            browser = self.parent_browser.current_browser()
            if browser:
                script = """
                (function() {
                    const perf = performance.timing;
                    const metrics = {
                        'Page Load Time': (perf.loadEventEnd - perf.navigationStart) + 'ms',
                        'DOM Ready': (perf.domContentLoadedEventEnd - perf.navigationStart) + 'ms',
                        'DNS Lookup': (perf.domainLookupEnd - perf.domainLookupStart) + 'ms',
                        'TCP Connection': (perf.connectEnd - perf.connectStart) + 'ms',
                        'Server Response': (perf.responseEnd - perf.requestStart) + 'ms',
                        'DOM Processing': (perf.domComplete - perf.domLoading) + 'ms'
                    };
                    return JSON.stringify(metrics, null, 2);
                })();
                """
                browser.page().runJavaScript(script, self.display_performance)
    
    def display_performance(self, metrics):
        """Display performance metrics"""
        if metrics:
            self.performance_display.setPlainText(f"⚡ Performance Metrics:\n\n{metrics}")
        else:
            self.performance_display.setPlainText("Performance data not available")


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
        
        # Create AI Chat side panel
        self.ai_panel = AIChatPanel(self)
        self.ai_panel.setMinimumWidth(300)
        self.ai_panel.setMaximumWidth(500)
        
        # Create Developer Tools panel
        self.devtools_panel = DevToolsPanel(self)
        self.devtools_panel.setMinimumHeight(200)
        
        # Create vertical splitter for main content and devtools
        self.vertical_splitter = QSplitter(Qt.Orientation.Vertical)
        self.vertical_splitter.addWidget(self.tabs)
        self.vertical_splitter.addWidget(self.devtools_panel)
        self.vertical_splitter.setStretchFactor(0, 3)  # Main content
        self.vertical_splitter.setStretchFactor(1, 1)  # DevTools
        
        # Create horizontal splitter for content and AI panel
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.vertical_splitter)
        self.splitter.addWidget(self.ai_panel)
        self.splitter.setStretchFactor(0, 3)  # Main content gets more space
        self.splitter.setStretchFactor(1, 1)  # Side panel gets less space
        
        # Initially hide panels
        self.ai_panel.hide()
        self.ai_panel_visible = False
        self.devtools_panel.hide()
        self.devtools_visible = False
        
        self.setCentralWidget(self.splitter)
        
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
        
        navbar.addSeparator()
        
        ai_panel_btn = QAction('🤖', self)
        ai_panel_btn.setToolTip('Toggle AI Chat Assistant')
        ai_panel_btn.triggered.connect(self.toggle_ai_panel)
        navbar.addAction(ai_panel_btn)
        
        devtools_btn = QAction('🔧', self)
        devtools_btn.setToolTip('Toggle Developer Tools')
        devtools_btn.triggered.connect(self.toggle_devtools)
        navbar.addAction(devtools_btn)
        
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
        
        devtools_action = QAction('🔧 Developer Tools', self)
        devtools_action.setShortcut(QKeySequence('F12'))
        devtools_action.triggered.connect(self.toggle_devtools)
        tools_menu.addAction(devtools_action)
        
        tools_menu.addSeparator()
        
        ai_chat_action = QAction('🤖 AI Chat Assistant', self)
        ai_chat_action.setShortcut(QKeySequence('Ctrl+Shift+A'))
        ai_chat_action.triggered.connect(self.toggle_ai_panel)
        tools_menu.addAction(ai_chat_action)
        
        tools_menu.addSeparator()
        
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
    
    def toggle_ai_panel(self):
        """Toggle AI Chat side panel visibility"""
        self.ai_panel_visible = not self.ai_panel_visible
        
        if self.ai_panel_visible:
            self.ai_panel.show()
        else:
            self.ai_panel.hide()
    
    def toggle_devtools(self):
        """Toggle Developer Tools panel visibility"""
        self.devtools_visible = not self.devtools_visible
        
        if self.devtools_visible:
            self.devtools_panel.show()
        else:
            self.devtools_panel.hide()
    
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
