# Pasty (페이스티)

Ghost-typing tool for practicing/mimicking code entry.
코드 입력을 연습하거나 흉내 내기 위한 고스트 타이핑 도구입니다.

## Description / 설명
Pasty is a creative tool that allows you to "type" code perfectly by pressing random keys. It's useful for demonstrating coding flows or practicing muscle memory without worrying about typos.
페이스티는 랜덤 키를 눌러 코드를 완벽하게 "입력"할 수 있게 해주는 창의적인 도구입니다. 코딩 흐름을 시연하거나 오타 걱정 없이 근육 기억을 연습하는 데 유용합니다.

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
pip install pynput Pillow
```

### Run / 실행
```bash
python3 main.py
```

## How to use / 사용 방법
1. Select a **Source** file (the code you "already wrote"). / "이미 작성한" 소스 파일을 선택합니다.
2. Select a **Target** file (where you will "pretend to type"). / "타이핑하는 척할" 대상 파일을 선택합니다.
3. Hold the **START** button. The indicator will turn red (**REC**). / **START** 버튼을 길게 누릅니다. 표시등이 빨간색(**REC**)으로 변합니다.
4. Type anything on your keyboard! The source text will appear in the target file as if you're typing it perfectly. / 키보드로 아무거나 입력하세요! 소스 텍스트가 마치 완벽하게 입력하는 것처럼 대상 파일에 나타납니다.

## License / 라이선스
Apache License 2.0

## Author / 제작자
Rheehose (Rhee Creative) 2008-2026
Website: https://rheehose.com
