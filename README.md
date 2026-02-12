# Pasty (페이스티)

Frutiger Aero styled ghost-typing tool built with PySide6.
PySide6로 제작된 프루티거 에어로 스타일 고스트 타이핑 도구.

## Features / 주요 기능
- **Ghost-typing**: Perfect typing simulation / 완벽한 타이핑 시뮬레이션
- **Frutiger Aero Design**: True gradient backgrounds with Qt / Qt로 구현한 진짜 그라디언트 배경
- **PySide6 (Qt)**: Modern, powerful UI framework / 현대적이고 강력한 UI 프레임워크
- **Theme/Language Toggle**: Light/Dark, KR/EN / 라이트/다크, 한/영
- **Settings Persistence**: Auto-generated settings.json / 자동 생성되는 settings.json

## Installation / 설치

```bash
# Clone / 클론
git clone https://github.com/hslcrb/pasty.git
cd pasty

# Virtual environment / 가상 환경
python3 -m venv venv
source venv/bin/activate

# Dependencies / 의존성
pip install PySide6 pynput darkdetect

# Generate assets / 에셋 생성
python3 create_assets.py
```

## Run / 실행
```bash
python3 main.py
```

## Build / 빌드
```bash
pip install pyinstaller
pyinstaller --onedir --noconsole --name pasty --icon=assets/icon.ico main.py
```

## Why PySide6? / 왜 PySide6인가?
- **QSS Stylesheets**: CSS-like styling with gradients / CSS 같은 스타일링과 그라디언트
- **Better Performance**: Native rendering / 네이티브 렌더링
- **Modern UI**: Premium look and feel / 프리미엄 외관과 느낌

## License / 라이선스
Apache License 2.0

## Author / 제작자
Rheehose (Rhee Creative) 2008-2026  
Website: https://rheehose.com
