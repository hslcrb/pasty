
"""
Pasty (페이스티) - Core Typing Engine
"""

import time
import random
import threading
from pynput import keyboard

class GhostTyper:
    def __init__(self, source_content, target_path=None):
        self.source_content = source_content
        self.target_path = target_path
        self.content_index = 0
        self.is_recording = False
        self.kb_controller = keyboard.Controller()
        self.listener = None
        self.on_status_change = None # Callback for UI updates

    def start(self):
        """Start listening for keyboard events"""
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

    def stop(self):
        """Stop listening"""
        if self.listener:
            self.listener.stop()

    def set_recording(self, state):
        """Set recording state"""
        self.is_recording = state
        if self.on_status_change:
            self.on_status_change(state)

    def _on_press(self, key):
        if not self.is_recording:
            return
        
        # Check for modifiers to avoid typing during shortcuts
        is_modifier = False
        if hasattr(key, 'name'):
            if any(mod in key.name for mod in ['ctrl', 'alt', 'shift', 'cmd', 'win']):
                is_modifier = True
        
        if not is_modifier:
            self._inject_chars()

    def _inject_chars(self):
        if not self.source_content or self.content_index >= len(self.source_content):
            return

        # Typer logic: 1-5 chars at a time
        num_chars = random.randint(1, 5)
        chars_to_add = self.source_content[self.content_index : self.content_index + num_chars]
        self.content_index += num_chars

        if chars_to_add:
            # Type in separate thread to not block listener
            threading.Thread(target=self._type_chars, args=(chars_to_add,), daemon=True).start()
            
            # Write to target file if set
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
