#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pasty (페이스티) - Ghost-typing Utility
Rheehose (Rhee Creative) 2008-2026
License: Apache License 2.0

This tool allows users to mimic typing a source text by pressing random keys.
이 도구는 사용자가 랜덤 키를 누를 때 소스 텍스트를 대상 파일에 흉내 내어 입력할 수 있게 해줍니다.
"""

import os
import sys
import random
import threading
import time
import tkinter as tk
from tkinter import filedialog, font, messagebox
from pynput import keyboard

# Constants / 상수
APP_NAME = "Pasty / 페이스티"
VERSION = "v0.1.0"  # Version up / 버전 업
COLOR_BG = "#121212"
COLOR_CARD = "#1E1E1E"
COLOR_ACCENT = "#BB86FC"
COLOR_REC = "#CF6679"
COLOR_TEXT_PRIMARY = "#E1E1E1"
COLOR_TEXT_SECONDARY = "#A0A0A0"

class PastyApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} {VERSION}")
        self.root.geometry("600x500")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)

        # State / 상태
        self.source_path = tk.StringVar(value="")
        self.target_path = tk.StringVar(value="")
        self.is_recording = False
        self.source_content = ""
        self.content_index = 0
        
        # Keyboard Controller / 키보드 컨트롤러
        self.kb_controller = keyboard.Controller()
        self.listener = None

        self.setup_ui()
        self.start_keyboard_listener()

    def setup_ui(self):
        try:
            self.title_font = font.Font(family="Inter", size=24, weight="bold")
            self.label_font = font.Font(family="Inter", size=10)
            self.path_font = font.Font(family="Roboto Mono", size=9)
            self.btn_font = font.Font(family="Inter", size=12, weight="bold")
        except:
            self.title_font = font.Font(family="sans-serif", size=24, weight="bold")
            self.label_font = font.Font(family="sans-serif", size=10)
            self.path_font = font.Font(family="monospace", size=9)
            self.btn_font = font.Font(family="sans-serif", size=12, weight="bold")

        header = tk.Frame(self.root, bg=COLOR_BG, pady=20)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="PASTY", font=self.title_font, fg=COLOR_ACCENT, bg=COLOR_BG).pack()
        tk.Label(header, text="Ghost-typing Mimic Tool / 고스트 타이핑 도구", font=self.label_font, fg=COLOR_TEXT_SECONDARY, bg=COLOR_BG).pack()

        container = tk.Frame(self.root, bg=COLOR_BG, padx=40)
        container.pack(fill=tk.BOTH, expand=True)

        # Source Selection
        source_frame = tk.Frame(container, bg=COLOR_BG, pady=10)
        source_frame.pack(fill=tk.X)
        tk.Label(source_frame, text="Source Text (File) / 원천 텍스트 (파일)", font=self.label_font, fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG).pack(anchor="w")
        entry_frame = tk.Frame(source_frame, bg=COLOR_CARD, padx=10, pady=5)
        entry_frame.pack(fill=tk.X, pady=5)
        self.source_label = tk.Label(entry_frame, textvariable=self.source_path, font=self.path_font, fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD, anchor="w")
        self.source_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(entry_frame, text="Browse / 찾아보기", font=self.label_font, bg=COLOR_ACCENT, fg=COLOR_BG, bd=0, padx=10, command=self.browse_source).pack(side=tk.RIGHT)

        # Target Selection / 대상 텍스트 선택
        target_frame = tk.Frame(container, bg=COLOR_BG, pady=10)
        target_frame.pack(fill=tk.X)
        tk.Label(target_frame, text="Target Text (Mandatory) / 대상 텍스트 (필수)", font=self.label_font, fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG).pack(anchor="w")
        entry_frame_t = tk.Frame(target_frame, bg=COLOR_CARD, padx=10, pady=5)
        entry_frame_t.pack(fill=tk.X, pady=5)
        self.target_label = tk.Label(entry_frame_t, textvariable=self.target_path, font=self.path_font, fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD, anchor="w")
        self.target_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(entry_frame_t, text="Browse / 찾아보기", font=self.label_font, bg=COLOR_ACCENT, fg=COLOR_BG, bd=0, padx=10, command=self.browse_target).pack(side=tk.RIGHT)

        self.rec_label = tk.Label(container, text="● REC", font=self.btn_font, fg=COLOR_BG, bg=COLOR_BG, pady=10)
        self.rec_label.pack()

        self.start_btn = tk.Button(container, text="READY", font=self.btn_font, bg=COLOR_CARD, fg=COLOR_TEXT_SECONDARY, activebackground=COLOR_REC, activeforeground=COLOR_BG, bd=0, pady=15, state=tk.DISABLED)
        self.start_btn.pack(fill=tk.X, pady=20)
        
        self.start_btn.bind("<ButtonPress-1>", self.on_press_start)
        self.start_btn.bind("<ButtonRelease-1>", self.on_release_start)

    def browse_source(self):
        file_path = filedialog.askopenfilename(title="Select Source File / 원천 파일 선택")
        if file_path:
            self.source_path.set(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.source_content = f.read()
                self.check_ready()
            except Exception as e:
                messagebox.showerror("Error / 오류", f"Failed to read file: {e}")

    def browse_target(self):
        file_path = filedialog.askopenfilename(title="Select Target File / 대상 파일 선택")
        if file_path:
            # Removed the empty file restriction as per user request
            self.target_path.set(file_path)
            self.check_ready()

    def check_ready(self):
        if self.source_path.get():
            self.start_btn.config(state=tk.NORMAL, text="HOLD TO START / 누르고 있으면 시작", bg=COLOR_ACCENT, fg=COLOR_BG)
        else:
            self.start_btn.config(state=tk.DISABLED, text="READY", bg=COLOR_CARD, fg=COLOR_TEXT_SECONDARY)

    def on_press_start(self, event):
        if self.start_btn['state'] == tk.NORMAL:
            self.is_recording = True
            self.start_btn.config(text="PASTING... / 복사 중...", bg=COLOR_REC)
            self.rec_label.config(fg=COLOR_REC)

    def on_release_start(self, event):
        self.is_recording = False
        self.start_btn.config(text="HOLD TO START / 누르고 있으면 시작", bg=COLOR_ACCENT)
        self.rec_label.config(fg=COLOR_BG)

    def start_keyboard_listener(self):
        def on_press(key):
            if not self.is_recording:
                return

            # Check if it's a modifier key / 수식 키(Ctrl, Alt 등)인지 확인
            is_modifier = False
            if hasattr(key, 'name'):
                if any(mod in key.name for mod in ['ctrl', 'alt', 'shift', 'cmd', 'win']):
                    is_modifier = True
            
            if not is_modifier:
                # Inject chars via keyboard simulation / 키보드 시뮬레이션으로 문자 주입
                self.inject_chars()
                # Stop original key if we want to "mimic perfectly" / 완벽히 흉내 내려면 원본 키 중단 가능
                # But here we just inject. If we want to SUPPRESS, we'd need to return False and restart.
                # Simplified: just inject.

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

    def inject_chars(self):
        if not self.source_content or self.content_index >= len(self.source_content):
            return

        num_chars = random.randint(1, 5)
        chars_to_add = self.source_content[self.content_index : self.content_index + num_chars]
        self.content_index += num_chars

        if chars_to_add:
            # Simulate typing / 타이핑 시뮬레이션
            # We use threading to avoid blocking the listener or GUI
            threading.Thread(target=self._type_chars, args=(chars_to_add,), daemon=True).start()
            
            # Optionally also write to file if target is specified
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
            print(f"Simulation Error / 시뮬레이션 오류: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PastyApp(root)
    copy_label = tk.Label(root, text="Rheehose (Rhee Creative) 2008-2026", font=("Inter", 8), bg=COLOR_BG, fg=COLOR_TEXT_SECONDARY)
    copy_label.pack(side=tk.BOTTOM, pady=10)
    root.mainloop()
