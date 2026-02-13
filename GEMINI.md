# Pasty Development Notes / Pasty 개발 노트

## Project Info / 프로젝트 정보
- Name: Pasty (페이스티)
- Type: Ghost-typing utility
- Version: v0.7.0
- Framework: PySide6
- License: Apache 2.0

## Design Evolution / 디자인 진화
1. **tkinter** - Initial attempt, transparency issues
2. **PySide6 + Frutiger Aero** - Complex gradient design
3. **PySide6 + Minimal Flat** - Final simple design ⭐

## Current Specs / 현재 사양
- Window: 500×450 (fixed)
- Background: Solid colors (#f5f5f5 / #1a1a1a)
- No icons, no complex gradients
- Material Blue accent (#2196F3)

## Features / 기능
- [x] Ghost-typing simulation
- [x] Light/Dark theme (auto-detected)
- [x] Korean/English language
- [x] Settings persistence
- [x] Clean minimal UI
- [x] CI/CD automation
- [x] **CLI Version** (v0.7.0)
- [x] **Manual Path Input** (v0.7.0)

## Development Commands / 개발 명령어
```bash
# Run GUI
python3 main.py

# Run CLI
python3 main_cli.py

# Test
# (manual testing required)

# Build
pyinstaller --onedir --windowed --name pasty main.py
```

## CI/CD
- Platform: GitHub Actions
- Builds: Ubuntu, Windows, macOS
- Trigger: Every push to master
- Output: ZIP packages per platform

## Notes / 참고사항
- No asset generation needed (no icons/backgrounds)
- Removed `create_assets.py` from workflow
- Settings auto-generated on first run

---
Rheehose (Rhee Creative) 2008-2026
