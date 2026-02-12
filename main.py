#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pasty (페이스티) - Ghost-typing Utility
Rheehose (Rhee Creative) 2008-2026
License: Apache License 2.0
"""

import os
import sys
import json
import random
import threading
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                QHBoxLayout, QLabel, QPushButton, QFileDialog, QFrame)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QPalette, QColor, QLinearGradient
from pynput import keyboard

try:
    import darkdetect
except ImportError:
    darkdetect = None

# Constants
APP_NAME = "Pasty"
VERSION = "v0.4.0"

# Language Strings
STRINGS = {
    "ko": {
        "title": "PASTY",
        "subtitle": "고스트 타이핑 도구",
        "source_label": "원천 텍스트 (파일)",
        "target_label": "대상 텍스트 (필수)",
        "browse": "찾아보기",
        "ready": "준비",
        "hold_to_start": "누르고 있으면 시작",
        "pasting": "복사 중...",
        "rec": "● REC",
        "error": "오류",
        "failed_read": "파일 읽기 실패",
        "copyright": "Rheehose (Rhee Creative) 2008-2026"
    },
    "en": {
        "title": "PASTY",
        "subtitle": "Ghost-typing Mimic Tool",
        "source_label": "Source Text (File)",
        "target_label": "Target Text (Mandatory)",
        "browse": "Browse",
        "ready": "READY",
        "hold_to_start": "HOLD TO START",
        "pasting": "PASTING...",
        "rec": "● REC",
        "error": "Error",
        "failed_read": "Failed to read file",
        "copyright": "Rheehose (Rhee Creative) 2008-2026"
    }
}

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
        self.apply_styles()
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
        """Setup UI elements"""
        self.setWindowTitle(f"{STRINGS[self.current_language]['title']} {VERSION}")
        self.setFixedSize(600, 550)
        
        # Set icon
        icon_path = Path("assets/icon.ico")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 20, 40, 20)
        main_layout.setSpacing(15)
        
        # Header with controls
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        
        self.theme_btn = QPushButton("◐")
        self.theme_btn.setObjectName("ctrlBtn")
        self.theme_btn.setFixedSize(40, 30)
        self.theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_btn)
        
        self.lang_btn = QPushButton("한/en")
        self.lang_btn.setObjectName("ctrlBtn")
        self.lang_btn.setFixedSize(60, 30)
        self.lang_btn.clicked.connect(self.toggle_language)
        header_layout.addWidget(self.lang_btn)
        
        main_layout.addLayout(header_layout)
        
        # Title
        self.title_label = QLabel()
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("subtitleLabel")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.subtitle_label)
        
        main_layout.addSpacing(20)
        
        # Source file
        self.source_label = QLabel()
        self.source_label.setObjectName("fieldLabel")
        main_layout.addWidget(self.source_label)
        
        source_layout = QHBoxLayout()
        self.source_path_label = QLabel("")
        self.source_path_label.setObjectName("pathLabel")
        source_layout.addWidget(self.source_path_label, 1)
        
        self.source_browse_btn = QPushButton()
        self.source_browse_btn.setObjectName("browseBtn")
        self.source_browse_btn.clicked.connect(self.browse_source)
        source_layout.addWidget(self.source_browse_btn)
        
        main_layout.addLayout(source_layout)
        
        # Target file
        self.target_label = QLabel()
        self.target_label.setObjectName("fieldLabel")
        main_layout.addWidget(self.target_label)
        
        target_layout = QHBoxLayout()
        self.target_path_label = QLabel("")
        self.target_path_label.setObjectName("pathLabel")
        target_layout.addWidget(self.target_path_label, 1)
        
        self.target_browse_btn = QPushButton()
        self.target_browse_btn.setObjectName("browseBtn")
        self.target_browse_btn.clicked.connect(self.browse_target)
        target_layout.addWidget(self.target_browse_btn)
        
        main_layout.addLayout(target_layout)
        
        main_layout.addSpacing(10)
        
        # REC indicator
        self.rec_label = QLabel()
        self.rec_label.setObjectName("recLabel")
        self.rec_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.rec_label)
        
        # Start button
        self.start_btn = QPushButton()
        self.start_btn.setObjectName("startBtn")
        self.start_btn.setFixedHeight(50)
        self.start_btn.setEnabled(False)
        self.start_btn.pressed.connect(self.on_press_start)
        self.start_btn.released.connect(self.on_release_start)
        main_layout.addWidget(self.start_btn)
        
        main_layout.addStretch()
        
        # Copyright
        self.copyright_label = QLabel()
        self.copyright_label.setObjectName("copyrightLabel")
        self.copyright_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.copyright_label)

    def apply_styles(self):
        """Apply QSS stylesheet with Frutiger Aero theme"""
        if self.resolved_theme == "dark":
            gradient_start = "#0A1628"
            gradient_end = "#1C3A52"
            text_primary = "#E8F4F8"
            text_secondary = "#8FB3D5"
            accent = "#4A90E2"
            card = "#1C2E4A"
            rec_color = "#E24A4A"
        else:
            gradient_start = "#87CEEB"
            gradient_end = "#E8F4F8"
            text_primary = "#1A3A52"
            text_secondary = "#5A7A8C"
            accent = "#2E7FC4"
            card = "#FFFFFF"
            rec_color = "#D32F2F"
        
        stylesheet = f"""
        QMainWindow {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {gradient_start}, stop:1 {gradient_end});
        }}
        
        QWidget {{
            background: transparent;
            color: {text_primary};
            font-family: 'Segoe UI', sans-serif;
        }}
        
        #titleLabel {{
            font-size: 28px;
            font-weight: bold;
            color: {accent};
        }}
        
        #subtitleLabel {{
            font-size: 11px;
            color: {text_secondary};
        }}
        
        #fieldLabel {{
            font-size: 10px;
            color: {text_primary};
            margin-top: 10px;
        }}
        
        #pathLabel {{
            background: {card};
            color: {text_secondary};
            padding: 8px 12px;
            border-radius: 4px;
            font-family: 'Consolas', monospace;
            font-size: 9px;
        }}
        
        #ctrlBtn {{
            background: {card};
            color: {text_primary};
            border: none;
            border-radius: 4px;
            font-size: 12px;
        }}
        
        #ctrlBtn:hover {{
            background: {accent};
        }}
        
        #browseBtn {{
            background: {accent};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-size: 10px;
            font-weight: bold;
        }}
        
        #browseBtn:hover {{
            background: {accent};
            opacity: 0.8;
        }}
        
        #recLabel {{
            font-size: 14px;
            font-weight: bold;
            color: {'transparent' if not self.is_recording else rec_color};
        }}
        
        #startBtn {{
            background: {accent if self.start_btn.isEnabled() else card};
            color: {'white' if self.start_btn.isEnabled() else text_secondary};
            border: none;
            border-radius: 6px;
            font-size: 13px;
            font-weight: bold;
        }}
        
        #startBtn:hover {{
            background: {rec_color if self.start_btn.isEnabled() else card};
        }}
        
        #startBtn:disabled {{
            background: {card};
            color: {text_secondary};
        }}
        
        #copyrightLabel {{
            font-size: 8px;
            color: {text_secondary};
        }}
        """
        
        self.setStyleSheet(stylesheet)

    def update_language(self):
        """Update all text with current language"""
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
        """Toggle theme"""
        if self.current_theme == "system":
            self.current_theme = "dark" if self.resolved_theme == "light" else "light"
        elif self.current_theme == "dark":
            self.current_theme = "light"
        else:
            self.current_theme = "dark"
        
        self.resolved_theme = self.current_theme
        self.apply_styles()
        self.save_settings()

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
            self.source_path_label.setText(file_path)
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
            self.target_path_label.setText(file_path)
            self.check_ready()

    def check_ready(self):
        s = STRINGS[self.current_language]
        if self.source_path and self.target_path:
            self.start_btn.setEnabled(True)
            self.start_btn.setText(s['hold_to_start'])
        else:
            self.start_btn.setEnabled(False)
            self.start_btn.setText(s['ready'])
        self.apply_styles()

    def on_press_start(self):
        if self.start_btn.isEnabled():
            s = STRINGS[self.current_language]
            self.is_recording = True
            self.start_btn.setText(s['pasting'])
            self.apply_styles()

    def on_release_start(self):
        s = STRINGS[self.current_language]
        self.is_recording = False
        self.start_btn.setText(s['hold_to_start'])
        self.apply_styles()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PastyApp()
    window.show()
    sys.exit(app.exec())
