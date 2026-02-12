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
import tkinter as tk
from tkinter import filedialog, font, messagebox
from pynput import keyboard
from pathlib import Path

try:
    import darkdetect
except ImportError:
    darkdetect = None

# Constants
APP_NAME = "Pasty"
VERSION = "v0.2.0"

# Theme Colors
THEMES = {
    "dark": {
        "bg": "#121212",
        "card": "#1E1E1E",
        "accent": "#BB86FC",
        "rec": "#CF6679",
        "text_primary": "#E1E1E1",
        "text_secondary": "#A0A0A0"
    },
    "light": {
        "bg": "#F5F5F5",
        "card": "#FFFFFF",
        "accent": "#6200EE",
        "rec": "#B00020",
        "text_primary": "#212121",
        "text_secondary": "#757575"
    }
}

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
        "theme_toggle_tooltip": "테마 전환",
        "lang_toggle_tooltip": "언어 전환",
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
        "theme_toggle_tooltip": "Toggle Theme",
        "lang_toggle_tooltip": "Toggle Language",
        "copyright": "Rheehose (Rhee Creative) 2008-2026"
    }
}

class PastyApp:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        
        # Settings
        self.settings_path = Path.home() / ".pasty_settings.json"
        self.load_settings()
        
        # State
        self.source_path = tk.StringVar(value="")
        self.target_path = tk.StringVar(value="")
        self.is_recording = False
        self.source_content = ""
        self.content_index = 0
        
        # Keyboard Controller
        self.kb_controller = keyboard.Controller()
        self.listener = None
        
        self.setup_ui()
        self.apply_theme()
        self.apply_language()
        self.start_keyboard_listener()

    def load_settings(self):
        """Load settings from JSON"""
        default_settings = {
            "theme": "system",
            "language": "ko"
        }
        
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
        # Fonts
        try:
            self.title_font = font.Font(family="Inter", size=24, weight="bold")
            self.label_font = font.Font(family="Inter", size=10)
            self.path_font = font.Font(family="Roboto Mono", size=9)
            self.btn_font = font.Font(family="Inter", size=12, weight="bold")
            self.icon_font = font.Font(family="Sans", size=14)
        except:
            self.title_font = font.Font(family="sans-serif", size=24, weight="bold")
            self.label_font = font.Font(family="sans-serif", size=10)
            self.path_font = font.Font(family="monospace", size=9)
            self.btn_font = font.Font(family="sans-serif", size=12, weight="bold")
            self.icon_font = font.Font(family="sans-serif", size=14)

        self.root.geometry("600x550")
        
        # Header with controls
        header = tk.Frame(self.root, pady=20)
        header.pack(fill=tk.X)
        
        # Theme and Language buttons
        controls_frame = tk.Frame(header)
        controls_frame.pack(side=tk.RIGHT, padx=20)
        
        self.theme_btn = tk.Button(controls_frame, text="◐", font=self.icon_font, bd=0, padx=8, pady=4, command=self.toggle_theme, cursor="hand2")
        self.theme_btn.pack(side=tk.LEFT, padx=2)
        
        self.lang_btn = tk.Button(controls_frame, text="한/en", font=self.label_font, bd=0, padx=8, pady=4, command=self.toggle_language, cursor="hand2")
        self.lang_btn.pack(side=tk.LEFT, padx=2)
        
        # Title
        self.title_label = tk.Label(header, font=self.title_font)
        self.title_label.pack()
        
        self.subtitle_label = tk.Label(header, font=self.label_font)
        self.subtitle_label.pack()

        # Main Container
        container = tk.Frame(self.root, padx=40)
        container.pack(fill=tk.BOTH, expand=True)

        # Source Selection
        source_frame = tk.Frame(container, pady=10)
        source_frame.pack(fill=tk.X)
        
        self.source_label_widget = tk.Label(source_frame, font=self.label_font)
        self.source_label_widget.pack(anchor="w")
        
        self.source_entry_frame = tk.Frame(source_frame, padx=10, pady=5)
        self.source_entry_frame.pack(fill=tk.X, pady=5)
        
        self.source_path_label = tk.Label(self.source_entry_frame, textvariable=self.source_path, font=self.path_font, anchor="w")
        self.source_path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.source_browse_btn = tk.Button(self.source_entry_frame, font=self.label_font, bd=0, padx=10, command=self.browse_source, cursor="hand2")
        self.source_browse_btn.pack(side=tk.RIGHT)

        # Target Selection
        target_frame = tk.Frame(container, pady=10)
        target_frame.pack(fill=tk.X)
        
        self.target_label_widget = tk.Label(target_frame, font=self.label_font)
        self.target_label_widget.pack(anchor="w")
        
        self.target_entry_frame = tk.Frame(target_frame, padx=10, pady=5)
        self.target_entry_frame.pack(fill=tk.X, pady=5)
        
        self.target_path_label = tk.Label(self.target_entry_frame, textvariable=self.target_path, font=self.path_font, anchor="w")
        self.target_path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.target_browse_btn = tk.Button(self.target_entry_frame, font=self.label_font, bd=0, padx=10, command=self.browse_target, cursor="hand2")
        self.target_browse_btn.pack(side=tk.RIGHT)

        # REC Indicator
        self.rec_label = tk.Label(container, font=self.btn_font, pady=10)
        self.rec_label.pack()

        # Start Button
        self.start_btn = tk.Button(container, font=self.btn_font, bd=0, pady=15, state=tk.DISABLED, cursor="hand2")
        self.start_btn.pack(fill=tk.X, pady=20)
        
        self.start_btn.bind("<ButtonPress-1>", self.on_press_start)
        self.start_btn.bind("<ButtonRelease-1>", self.on_release_start)
        
        # Copyright
        self.copyright_label = tk.Label(self.root, font=("Inter", 8), pady=10)
        self.copyright_label.pack(side=tk.BOTTOM)

    def apply_theme(self):
        """Apply current theme colors"""
        theme = THEMES[self.resolved_theme]
        
        # Root and frames
        self.root.configure(bg=theme["bg"])
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=theme["bg"])
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        child.configure(bg=theme["bg"])
        
        # Header elements
        self.title_label.configure(fg=theme["accent"], bg=theme["bg"])
        self.subtitle_label.configure(fg=theme["text_secondary"], bg=theme["bg"])
        
        # Control buttons
        self.theme_btn.configure(bg=theme["card"], fg=theme["text_primary"], activebackground=theme["accent"])
        self.lang_btn.configure(bg=theme["card"], fg=theme["text_primary"], activebackground=theme["accent"])
        
        # Labels
        self.source_label_widget.configure(fg=theme["text_primary"], bg=theme["bg"])
        self.target_label_widget.configure(fg=theme["text_primary"], bg=theme["bg"])
        
        # Entry frames and labels
        self.source_entry_frame.configure(bg=theme["card"])
        self.source_path_label.configure(fg=theme["text_secondary"], bg=theme["card"])
        self.source_browse_btn.configure(bg=theme["accent"], fg=theme["bg"], activebackground=theme["accent"])
        
        self.target_entry_frame.configure(bg=theme["card"])
        self.target_path_label.configure(fg=theme["text_secondary"], bg=theme["card"])
        self.target_browse_btn.configure(bg=theme["accent"], fg=theme["bg"], activebackground=theme["accent"])
        
        # REC label
        if self.is_recording:
            self.rec_label.configure(fg=theme["rec"], bg=theme["bg"])
        else:
            self.rec_label.configure(fg=theme["bg"], bg=theme["bg"])
        
        # Start button
        if self.start_btn['state'] == tk.NORMAL:
            self.start_btn.configure(bg=theme["accent"], fg=theme["bg"], activebackground=theme["rec"])
        else:
            self.start_btn.configure(bg=theme["card"], fg=theme["text_secondary"])
        
        # Copyright
        self.copyright_label.configure(bg=theme["bg"], fg=theme["text_secondary"])

    def apply_language(self):
        """Apply current language strings"""
        s = STRINGS[self.current_language]
        
        self.root.title(f"{s['title']} {VERSION}")
        self.title_label.configure(text=s['title'])
        self.subtitle_label.configure(text=s['subtitle'])
        self.source_label_widget.configure(text=s['source_label'])
        self.target_label_widget.configure(text=s['target_label'])
        self.source_browse_btn.configure(text=s['browse'])
        self.target_browse_btn.configure(text=s['browse'])
        self.rec_label.configure(text=s['rec'])
        self.copyright_label.configure(text=s['copyright'])
        
        if self.start_btn['state'] == tk.NORMAL:
            self.start_btn.configure(text=s['hold_to_start'])
        else:
            self.start_btn.configure(text=s['ready'])

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.current_theme == "system":
            self.current_theme = "dark" if self.resolved_theme == "light" else "light"
        elif self.current_theme == "dark":
            self.current_theme = "light"
        else:
            self.current_theme = "dark"
        
        self.resolved_theme = self.current_theme
        self.apply_theme()
        self.save_settings()

    def toggle_language(self):
        """Toggle between Korean and English"""
        self.current_language = "en" if self.current_language == "ko" else "ko"
        self.apply_language()
        self.save_settings()

    def browse_source(self):
        s = STRINGS[self.current_language]
        file_path = filedialog.askopenfilename(title=s['source_label'])
        if file_path:
            self.source_path.set(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.source_content = f.read()
                self.check_ready()
            except Exception as e:
                messagebox.showerror(s['error'], f"{s['failed_read']}: {e}")

    def browse_target(self):
        s = STRINGS[self.current_language]
        file_path = filedialog.askopenfilename(title=s['target_label'])
        if file_path:
            self.target_path.set(file_path)
            self.check_ready()

    def check_ready(self):
        s = STRINGS[self.current_language]
        if self.source_path.get() and self.target_path.get():
            self.start_btn.config(state=tk.NORMAL, text=s['hold_to_start'])
            self.apply_theme()
        else:
            self.start_btn.config(state=tk.DISABLED, text=s['ready'])
            self.apply_theme()

    def on_press_start(self, event):
        if self.start_btn['state'] == tk.NORMAL:
            s = STRINGS[self.current_language]
            self.is_recording = True
            self.start_btn.config(text=s['pasting'])
            self.apply_theme()

    def on_release_start(self, event):
        s = STRINGS[self.current_language]
        self.is_recording = False
        self.start_btn.config(text=s['hold_to_start'])
        self.apply_theme()

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
            
            if self.target_path.get():
                try:
                    with open(self.target_path.get(), 'a', encoding='utf-8') as f:
                        f.write(chars_to_add)
                except:
                    pass

    def _type_chars(self, chars):
        try:
            self.kb_controller.type(chars)
        except Exception as e:
            print(f"Simulation Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PastyApp(root)
    root.mainloop()
