# Pasty (페이스티)

Frutiger Aero styled ghost-typing tool with premium blue aesthetics.
프리미엄 블루 미학의 프루티거 에어로 스타일 고스트 타이핑 도구.

## Features / 주요 기능
- **Ghost-typing**: Perfect typing simulation at cursor / 커서 위치에서 완벽한 타이핑 시뮬레이션
- **Frutiger Aero Design**: Sky blue gradient background / 하늘색 그라디언트 배경
- **Theme Switching**: Light/Dark modes with system default / 시스템 기본값이 있는 라이트/다크 모드
- **Language Toggle**: Korean/English switching / 한국어/영어 전환
- **Settings Persistence**: Auto-generated settings.json / 자동 생성되는 settings.json

## Installation & Execution / 설치 및 실행

### Prerequisites / 사전 요구 사항
- Python 3.10+
- PIL/Pillow for image processing / 이미지 처리용 Pillow
- Accessibility permissions for keyboard listener / 키보드 리스너용 접근성 권한

### Setup / 설정
```bash
# Clone repository / 리포지토리 클론
git clone https://github.com/hslcrb/pasty.git
cd pasty

# Virtual environment / 가상 환경
python3 -m venv venv
source venv/bin/activate

# Dependencies / 의존성
pip install pynput Pillow darkdetect

# Generate assets (first time only) / 에셋 생성 (첫 실행 시)
python3 create_assets.py
```

### Run / 실행
```bash
python3 main.py
```

### Build / 빌드
```bash
pip install pyinstaller
pyinstaller --onedir --noconsole --name pasty --icon=assets/icon.ico main.py
# Output: dist/pasty/
```

## Usage / 사용 방법
1. **Select Source**: Code file to mimic / 흉내 낼 코드 파일
2. **Select Target**: Where to type (mandatory) / 타이핑할 위치 (필수)
3. **Customize**: Toggle theme (◐) and language (한/en) / 테마 및 언어 전환
4. **Hold START**: Press and hold, then type random keys / 버튼을 누른 상태에서 아무 키나 입력
5. **Magic**: Source appears perfectly at cursor! / 커서 위치에 소스가 완벽하게 나타남!

## Settings / 설정
`settings.json` is auto-created in project directory:
```json
{
  "theme": "system",
  "language": "ko"
}
```

## License / 라이선스
Apache License 2.0

## Author / 제작자
Rheehose (Rhee Creative) 2008-2026  
Website: https://rheehose.com
