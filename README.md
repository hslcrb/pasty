# Pasty (페이스티)

Minimal flat design ghost-typing tool built with PySide6.
PySide6로 제작된 미니멀 플랫 디자인 고스트 타이핑 도구.

## Features / 주요 기능
- **Ghost-typing**: Perfect typing simulation at cursor position / 커서 위치에서 완벽한 타이핑 시뮬레이션
- **Minimal Design**: Clean, simple flat UI / 깔끔하고 심플한 플랫 UI
- **PySide6 (Qt)**: Modern UI framework / 현대적인 UI 프레임워크
- **Theme Support**: Light and Dark modes / 라이트 및 다크 모드
- **Language Support**: Korean and English / 한국어 및 영어
- **Settings Persistence**: Auto-generated settings.json / 자동 생성되는 settings.json
- **CLI Support**: Terminal interface using `rich` / `rich`를 사용한 터미널 인터페이스 (v0.7.0)
- **Manual Path Input**: Direct typing of file paths / 파일 경로 직접 입력 (v0.7.0)

## Installation / 설치

```bash
# Clone / 클론
git clone https://github.com/hslcrb/pasty.git
cd pasty

# Virtual environment / 가상 환경
python3 -m venv venv
source venv/bin/activate

# Dependencies / 의존성
pip install -r requirements.txt
```

## Run / 실행
# GUI
python3 main.py

# CLI
python3 main_cli.py
python3 main_cli.py [source_file]
```

## Build / 빌드
```bash
pip install pyinstaller
pyinstaller --onedir --windowed --name pasty main.py
```

## Usage / 사용법
1. **Select Source File** / 원천 파일 선택: Browse or type the path to the text file / 텍스트 파일 경로를 찾거나 직접 입력
2. **Select Target File** / 대상 파일 선택: Browse or type where to save / 저장할 경로를 찾거나 직접 입력
3. **Hold Button** / 버튼 누르기: Press and hold the start button
4. **Type Naturally** / 자연스럽게 타이핑: While holding, type on your keyboard - each keystroke will inject 1-5 random characters from the source

## Technical Details / 기술 세부사항
- **UI Framework**: PySide6 (Qt for Python)
- **Keyboard Control**: pynput
- **Image Processing**: Pillow
- **Theme Detection**: darkdetect
- **Window Size**: 500×450 (fixed)
- **Design**: Minimal flat with solid backgrounds

## License / 라이선스
Apache License 2.0

## Author / 제작자
Rheehose (Rhee Creative) 2008-2026  
Website: https://rheehose.com
