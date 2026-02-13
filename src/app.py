
"""
Pasty (페이스티) - Main Application Logic
"""

import os
import sys
import json
import random
import threading
from pathlib import Path

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                QHBoxLayout, QLabel, QPushButton, QFileDialog, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPalette, QBrush
from pynput import keyboard

try:
    import darkdetect
except ImportError:
    darkdetect = None

from src.config import APP_NAME, VERSION, STRINGS

class PastyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Settings
        self.settings_path = Path("settings.json")
        self.load_settings()
        
        # State
        self.source_path = ""
        self.target_path = ""
        self.is_recording = False
        self.source_content = ""
        self.content_index = 0
        
        # Keyboard Controller
        self.kb_controller = keyboard.Controller()
        self.listener = None
        
        self.setup_ui()
        self.update_language()
        self.start_keyboard_listener()

    def load_settings(self):
        """Load settings from JSON, create if doesn't exist"""
        if self.settings_path.exists():
            try:
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.current_theme = settings.get("theme", "system")
                    self.current_language = settings.get("language", "ko")
            except:
                self.current_theme = "system"
                self.current_language = "ko"
        else:
            self.current_theme = "system"
            self.current_language = "ko"
            self.save_settings()
        
        # Resolve system theme
        if self.current_theme == "system":
            if darkdetect and darkdetect.isDark():
                self.resolved_theme = "dark"
            else:
                self.resolved_theme = "light"
        else:
            self.resolved_theme = self.current_theme

    def save_settings(self):
        """Save settings to JSON"""
        settings = {
            "theme": self.current_theme,
            "language": self.current_language
        }
        try:
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def setup_ui(self):
        """Setup minimal flat UI with Frutiger Aero buttons"""
        self.setWindowTitle(f"{STRINGS[self.current_language]['title']} {VERSION}")
        self.setFixedSize(500, 450)
        
        # Simple solid background
        if self.resolved_theme == "dark":
            self.setStyleSheet("QMainWindow { background-color: #1a1a1a; }")
        else:
            self.setStyleSheet("QMainWindow { background-color: #f5f5f5; }")
        
        # Central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(12)
        
        # Minimal colors
        if self.resolved_theme == "dark":
            text_color = "#ffffff"
            secondary_color = "#999999"
            accent_color = "#2196F3"
            card_color = "#2a2a2a"
            rec_color = "#f44336"
        else:
            text_color = "#333333"
            secondary_color = "#666666"
            accent_color = "#2196F3"
            card_color = "#ffffff"
            rec_color = "#f44336"
        
        # Title (no header controls)
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(f"font-size: 24px; font-weight: 600; color: {text_color}; margin: 10px;")
        main_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel()
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet(f"font-size: 12px; color: {secondary_color}; margin-bottom: 15px;")
        main_layout.addWidget(self.subtitle_label)
        
        # Source file
        self.source_label = QLabel()
        self.source_label.setStyleSheet(f"font-size: 11px; color: {text_color}; margin-top: 5px;")
        main_layout.addWidget(self.source_label)
        
        source_layout = QHBoxLayout()
        self.source_path_label = QLabel("")
        
        # Frutiger Aero Style
        if self.resolved_theme == "dark":
            input_style = """
                QLabel {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #333333, stop:1 #2a2a2a);
                    color: #e0e0e0;
                    border: 1px solid #555;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 11px;
                }
            """
            btn_style = """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4a90e2, stop:0.5 #357abd, stop:1 #2a68a8);
                    color: white;
                    border: 1px solid #1a4b78;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 11px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5ca0f2, stop:0.5 #4a90e2, stop:1 #357abd);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2a68a8, stop:1 #357abd);
                    padding-top: 9px;
                    padding-left: 17px;
                }
            """
            start_btn_style = """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4a90e2, stop:0.5 #357abd, stop:1 #2a68a8);
                    color: white;
                    border: 1px solid #1a4b78;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5ca0f2, stop:0.5 #4a90e2, stop:1 #357abd);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2a68a8, stop:1 #357abd);
                    padding-top: 2px;
                    padding-left: 2px;
                }
                QPushButton:disabled {
                    background: #2a2a2a;
                    color: #555;
                    border: 1px solid #444;
                }
            """
        else:
            input_style = """
                QLabel {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #f0f0f0);
                    color: #333333;
                    border: 1px solid #ccc;
                    border-bottom: 1px solid #bbb;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 11px;
                }
            """
            btn_style = """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #eefeff, stop:0.5 #d0f0ff, stop:1 #b0dfff);
                    color: #004488;
                    border: 1px solid #88ccee;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 11px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:0.5 #e0f5ff, stop:1 #cceeff);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #b0dfff, stop:1 #d0f0ff);
                    padding-top: 9px;
                    padding-left: 17px;
                }
            """
            start_btn_style = """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8accff, stop:0.5 #59aaff, stop:1 #4090ee);
                    color: white;
                    border: 1px solid #3070cc;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                    text-shadow: 0px 1px 1px rgba(0,0,0,0.3);
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a0d8ff, stop:0.5 #70b8ff, stop:1 #50a0ff);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4090ee, stop:1 #59aaff);
                    padding-top: 2px;
                    padding-left: 2px;
                }
                QPushButton:disabled {
                    background: #f0f0f0;
                    color: #aaa;
                    border: 1px solid #ccc;
                }
            """

        self.source_path_label.setStyleSheet(input_style)
        source_layout.addWidget(self.source_path_label, 1)
        
        self.source_browse_btn = QPushButton()
        self.source_browse_btn.setStyleSheet(btn_style)
        self.source_browse_btn.setCursor(Qt.PointingHandCursor)
        self.source_browse_btn.clicked.connect(self.browse_source)
        source_layout.addWidget(self.source_browse_btn)
        
        main_layout.addLayout(source_layout)
        
        # Target file
        self.target_label = QLabel()
        self.target_label.setStyleSheet(f"font-size: 11px; color: {text_color}; margin-top: 10px;")
        main_layout.addWidget(self.target_label)
        
        target_layout = QHBoxLayout()
        self.target_path_label = QLabel("")
        self.target_path_label.setStyleSheet(input_style)
        target_layout.addWidget(self.target_path_label, 1)
        
        self.target_browse_btn = QPushButton()
        self.target_browse_btn.setStyleSheet(btn_style)
        self.target_browse_btn.setCursor(Qt.PointingHandCursor)
        self.target_browse_btn.clicked.connect(self.browse_target)
        
        target_layout.addWidget(self.target_browse_btn)
        
        main_layout.addLayout(target_layout)
        
        # REC indicator
        self.rec_label = QLabel()
        self.rec_label.setAlignment(Qt.AlignCenter)
        self.rec_label.setStyleSheet(f"font-size: 13px; font-weight: 600; color: transparent; margin: 10px;")
        main_layout.addWidget(self.rec_label)
        
        # Start button
        self.start_btn = QPushButton()
        self.start_btn.setFixedHeight(50)
        self.start_btn.setEnabled(False)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        
        self.start_btn.setStyleSheet(start_btn_style)
        self.start_btn_style_normal = start_btn_style  # Save for logic use
        self.start_btn_style_disabled = start_btn_style.replace("QPushButton {", "QPushButton { /* disabled override */") # Hacky but handled by disabled state in CSS above
        self.start_btn.pressed.connect(self.on_press_start)
        self.start_btn.released.connect(self.on_release_start)
        main_layout.addWidget(self.start_btn)
        
        self.rec_color_style = rec_color
        
        main_layout.addStretch()
        
        # Copyright
        self.copyright_label = QLabel()
        self.copyright_label.setAlignment(Qt.AlignCenter)
        self.copyright_label.setStyleSheet(f"font-size: 9px; color: {secondary_color}; margin-top: 10px;")
        main_layout.addWidget(self.copyright_label)

    def update_language(self):
        """Update all text"""
        s = STRINGS[self.current_language]
        
        self.setWindowTitle(f"{s['title']} {VERSION}")
        self.title_label.setText(s['title'])
        self.subtitle_label.setText(s['subtitle'])
        self.source_label.setText(s['source_label'])
        self.target_label.setText(s['target_label'])
        self.source_browse_btn.setText(s['browse'])
        self.target_browse_btn.setText(s['browse'])
        self.rec_label.setText(s['rec'])
        self.copyright_label.setText(s['copyright'])
        
        if self.start_btn.isEnabled():
            self.start_btn.setText(s['hold_to_start'])
        else:
            self.start_btn.setText(s['ready'])

    def toggle_theme(self):
        """Toggle theme and restart"""
        # ... existing logic ...
        # (This button was removed in minimal design but method kept if needed for future)
        if self.current_theme == "system":
            self.current_theme = "dark" if self.resolved_theme == "light" else "light"
        elif self.current_theme == "dark":
            self.current_theme = "light"
        else:
            self.current_theme = "dark"
        
        self.resolved_theme = self.current_theme
        self.save_settings()
        
        # Restart app to apply theme
        QApplication.quit()
        os.execv(sys.executable, ['python3'] + sys.argv)

    def toggle_language(self):
        """Toggle language"""
        self.current_language = "en" if self.current_language == "ko" else "ko"
        self.update_language()
        self.save_settings()

    def browse_source(self):
        s = STRINGS[self.current_language]
        file_path, _ = QFileDialog.getOpenFileName(self, s['source_label'])
        if file_path:
            self.source_path = file_path
            self.source_path_label.setText(os.path.basename(file_path)) # Show basename
            self.source_path_label.setToolTip(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.source_content = f.read()
                self.content_index = 0
                self.check_ready()
            except Exception as e:
                print(f"Failed to read: {e}")

    def browse_target(self):
        s = STRINGS[self.current_language]
        file_path, _ = QFileDialog.getOpenFileName(self, s['target_label'])
        if file_path:
            self.target_path = file_path
            self.target_path_label.setText(os.path.basename(file_path))
            self.target_path_label.setToolTip(file_path)
            self.check_ready()

    def check_ready(self):
        s = STRINGS[self.current_language]
        if self.source_path and self.target_path:
            self.start_btn.setEnabled(True)
            self.start_btn.setText(s['hold_to_start'])
            self.start_btn.setStyleSheet(self.start_btn_style_normal)
        else:
            self.start_btn.setEnabled(False)
            self.start_btn.setText(s['ready'])
            self.start_btn.setStyleSheet(self.start_btn_style_disabled)

    def on_press_start(self):
        if self.start_btn.isEnabled():
            s = STRINGS[self.current_language]
            self.is_recording = True
            self.start_btn.setText(s['pasting'])
            self.rec_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {self.rec_color_style};")

    def on_release_start(self):
        s = STRINGS[self.current_language]
        self.is_recording = False
        self.start_btn.setText(s['hold_to_start'])
        self.rec_label.setStyleSheet("font-size: 14px; font-weight: bold; color: transparent;")

    def start_keyboard_listener(self):
        def on_press(key):
            if not self.is_recording:
                return
            
            is_modifier = False
            if hasattr(key, 'name'):
                if any(mod in key.name for mod in ['ctrl', 'alt', 'shift', 'cmd', 'win']):
                    is_modifier = True
            
            if not is_modifier:
                self.inject_chars()

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

    def inject_chars(self):
        if not self.source_content or self.content_index >= len(self.source_content):
            return

        num_chars = random.randint(1, 5)
        chars_to_add = self.source_content[self.content_index : self.content_index + num_chars]
        self.content_index += num_chars

        if chars_to_add:
            threading.Thread(target=self._type_chars, args=(chars_to_add,), daemon=True).start()
            
            if self.target_path:
                try:
                    with open(self.target_path, 'a', encoding='utf-8') as f:
                        f.write(chars_to_add)
                except:
                    pass

    def _type_chars(self, chars):
        try:
            self.kb_controller.type(chars)
        except Exception as e:
            print(f"Simulation Error: {e}")
