# Pasty (페이스티)

Ghost-typing tool with theme and language customization.
테마 및 언어 사용자 정의 기능이 있는 고스트 타이핑 도구입니다.

## Features / 주요 기능
- **Ghost-typing**: Simulate perfect typing at cursor position / 커서 위치에서 완벽한 타이핑 시뮬레이션
- **Theme Switching**: Light/Dark modes with system default / 시스템 기본값이 있는 라이트/다크 모드
- **Language Toggle**: Switch between Korean and English / 한국어와 영어 간 전환
- **Settings Persistence**: Preferences saved in JSON / JSON으로 설정 저장

## Installation & Execution / 설치 및 실행

### Prerequisites / 사전 요구 사항
- Python 3.10+
- Accessibility permissions (for global keyboard listener) / 접근성 권한 (전역 키보드 리스너용)

### Setup / 설정
```bash
# Clone the repository / 리포지토리 클론
git clone https://github.com/hslcrb/pasty.git
cd pasty

# Create and activate virtual environment / 가상 환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies / 의존성 설치
pip install pynput Pillow darkdetect
```

### Run / 실행
```bash
python3 main.py
```

### Build Executable / 실행 파일 빌드
```bash
pip install pyinstaller
pyinstaller --onedir --noconsole --name pasty main.py
# Output in: dist/pasty/
```

## How to use / 사용 방법
1. **Select Source**: Choose the code file you "already wrote" / "이미 작성한" 코드 파일 선택
2. **Select Target**: Choose where you'll "pretend to type" (mandatory) / "타이핑하는 척할" 위치 선택 (필수)
3. **Customize**: Toggle theme (◐) and language (한/en) as needed / 필요에 따라 테마 및 언어 전환
4. **Hold START**: Press and hold the button - indicator turns red (REC) / 버튼을 길게 누르면 빨간색(REC)으로 표시
5. **Type Anything**: Press random keys and watch the source appear perfectly! / 아무 키나 누르면 소스가 완벽하게 나타납니다!

## Settings / 설정
Preferences are stored in `~/.pasty_settings.json`:
```json
{
  "theme": "system",  // "light", "dark", or "system"
  "language": "ko"    // "ko" or "en"
}
```

## License / 라이선스
Apache License 2.0

## Author / 제작자
Rheehose (Rhee Creative) 2008-2026  
Website: https://rheehose.com
