# 4D 회전 테서랙트 (Rotating Tesseract)

파이썬과 Pygame을 사용하여 구현한 4차원 초입방체(테서랙트) 시각화 프로그램입니다. 사용자는 슬라이더를 통해 각 차원 평면(ZW, XW, XY)에서의 회전 속도와 크기를 조절할 수 있습니다.

## 기능 (Features)
- **4D 시각화**: 4차원 도형을 3차원으로, 다시 2차원으로 투영하여 화면에 표시합니다.
- **슬라이더 제어**: 
    - **Speed ZW, XW, XY**: 각 평면에서의 회전 속도를 조절합니다. 슬라이더를 왼쪽으로 밀면 역방향으로 회전합니다.
    - **Scale**: 도형의 크기(줌)를 조절합니다. 최대 1000까지 확대 가능합니다.
- **초기화 (Reset)**: 각 슬라이더 옆의 빨간색 "R" 버튼을 누르면 해당 값이 기본값(속도는 0, 크기는 250)으로 초기화됩니다.
- **웹 버전**: 웹어셈블리(WebAssembly)로 빌드되어 브라우저에서 바로 실행할 수 있습니다.

## 웹어셈블리 빌드 과정 (Detailed WebAssembly Build Process)

이 프로젝트는 **Pygbag**을 사용하여 Python/Pygame 코드를 웹어셈블리(WebAssembly)로 변환하였습니다. 빌드 및 배포 과정은 다음과 같습니다.

### 1. 도구 및 환경 (Tools & Environment)
- **Engine**: Chrome V8 (브라우저 실행 환경)
- **Build Tool**: [Pygbag](https://github.com/pygame-web/pygbag)
- **Language**: Python 3.12+

### 2. 빌드 준비 (Preparation)
웹 빌드를 위해 프로젝트 구조를 다음과 같이 구성했습니다.
- **`web_src/` 폴더**: 웹 빌드에 필요한 소스 코드를 별도 폴더로 분리합니다.
- **`main.py`**: 진입점 파일의 이름은 반드시 `main.py`여야 합니다. 기존 `rotating_tesseract.py`를 `main.py`로 변경하거나 복사하여 사용합니다.
- **`asyncio` 적용**: 웹 환경에서는 이벤트 루프가 브라우저를 차단하지 않도록 `asyncio`를 사용하여 메인 루프를 비동기로 작성해야 합니다. (코드 내 `async def run()`, `await asyncio.sleep(0)` 등 적용됨)

### 3. 빌드 명령 (Build Command)
터미널에서 다음 명령어를 실행하여 빌드합니다. `pygbag`은 소스 코드를 분석하고 필요한 자산(assets)을 패키징하여 웹 실행 가능한 형태로 변환합니다.

```bash
# 1. Pygbag 설치
pip install pygbag

# 2. 빌드 실행 (web_src 폴더를 지정)
pygbag web_src
```

### 4. 결과물 (Output)
빌드가 완료되면 `build/web/` 폴더가 생성됩니다.
- `index.html`: 웹 실행을 위한 메인 HTML 파일
- `web_src.apk`: 파이썬 코드와 자산이 패키징된 파일
- `python home`: 브라우저 내 가상 환경 파일들

### 5. 배포 (Deployment)
GitHub Pages 배포를 위해 빌드된 `build/web/` 내부의 파일들을 프로젝트 루트의 **`docs/`** 폴더로 이동시켰습니다.
GitHub Pages는 기본적으로 `docs/` 폴더를 웹 루트로 인식하도록 설정할 수 있기 때문입니다.

## 실행 방법 (How to Run)

### 1. 데스크탑 버전 (Python)
필요한 라이브러리를 설치하고 실행합니다.

```bash
pip install pygame
python rotating_tesseract.py
```

### 2. 웹 버전 (Web/GitHub Pages)
이 프로젝트는 `docs/` 폴더에 웹어셈블리 빌드 파일을 포함하고 있어 GitHub Pages를 통해 쉽게 배포할 수 있습니다.

#### GitHub Pages 설정 방법:
1. 이 레포지토리를 GitHub에 업로드합니다 ( **`docs/` 폴더가 반드시 포함되어야 합니다**).
2. GitHub 레포지토리 페이지에서 **Settings (설정)** 탭으로 이동합니다.
3. 왼쪽 사이드바에서 **Pages**를 클릭합니다.
4. **Build and deployment** 섹션의 **Source**에서 **Deploy from a branch**를 선택합니다.
5. **Branch** 항목에서 `main` (또는 사용하는 브랜치)를 선택하고, 폴더를 `/(root)` 대신 **`/docs`** 로 변경합니다.
6. **Save (저장)** 버튼을 클릭합니다.

잠시 후 상단에 생성된 URL을 통해 웹 브라우저에서 프로그램을 실행할 수 있습니다.
