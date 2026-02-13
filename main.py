
"""
Pasty (페이스티) - Ghost-typing Utility
Rheehose (Rhee Creative) 2008-2026
License: Apache License 2.0
"""

import sys
from PySide6.QtWidgets import QApplication
from src.app import PastyApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PastyApp()
    window.show()
    sys.exit(app.exec())
