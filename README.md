# ✨ Cammoji (캠모지)

<table align="center" width="100%">
  <tr>
    <td align="center" width="90px">
      <img src="./frontend/public/favicon.svg" width="70px" alt="Cammoji Favicon" />
    </td>
    <td>
      <b>"카메라 속 현실의 나와 사물을 가상 공간의 이모지 아바타로 실시간 동기화하다."</b><br />
      YOLO11 객체 인식과 WebSocket을 활용한 <b>실시간 인터랙티브 버추얼 아바타 스테이지</b>
    </td>
  </tr>
</table>

<br />

## 📖 프로젝트 소개 (진행 이유)

<table align="center" width="100%">
  <tr>
    <td align="center" width="30%">
      <img alt="cammoji_preview" src="https://github.com/user-attachments/assets/71f9f0b2-184c-4f5d-ae9a-cbe103449912" width="100%" alt="Cammoji Live Scene Preview" style="border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.4);" />
    </td>
    <td width="55%">
      복잡한 모션 캡처 장비나 무거운 3D 트래킹 툴 없이도, <b>"일반 웹캠 하나만으로 현실의 행동과 주변 사물을 가상 공간에 실시간으로 표현할 수 없을까?"</b>라는 아이디어에서 출발했습니다.<br /><br />
      <b>Cammoji</b>는 웹캠을 통해 사용자와 주변 사물(의자, 컵, 스마트폰, 노트북, 반려동물 등)을 AI로 실시간 탐지하고, 이를 웹 대시보드 상에서 레이어링(Z-Index)된 <b>인터랙티브 이모지 아바타</b>로 즉각 변환하여 보여주는 프로젝트입니다.
    </td>
  </tr>
</table>


---

## 👩‍💻 개발자 프로필 (Developer)

<table align="center" width="100%">
  <tr>
    <td align="center" width="160px">
      <img src="https://github.com/gjdbsdk.png" width="130px" style="border-radius: 50%;" alt="허윤아 프로필" />
      <br />
      <b>허윤아 (Yuna Heo)</b>
    </td>
    <td>
      <b>Role</b>: 1인 기획 & Full-stack / AI 개발 (100% Solo Project)<br /><br />
      <b>Contact</b>:<br />
      <a href="https://github.com/gjdbsdk"><img src="https://img.shields.io/badge/github-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub" /></a>
      <a href="mailto:aquahua0409@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?style=flat-square&logo=gmail&logoColor=white" alt="Gmail" /></a>
      <a href="https://discordapp.com/users/810888409039765518"><img src="https://img.shields.io/badge/Discord-5865F2?style=flat-square&logo=discord&logoColor=white" alt="Discord" /></a>
      <br /><br />
      <b>Stacks</b>:<br />
      <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=TypeScript&logoColor=white" alt="TS" />
      <img src="https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB" alt="React" />
      <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
      <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
      <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white" alt="OpenCV" />
    </td>
  </tr>
</table>

### 🛠️ 역할 및 기여도 (100% Solo Project)
- **Architecture:** Monorepo(Concurrently) 기반 FastAPI 백엔드와 React 프론트엔드 단일 파이프라인 구축
- **Backend & AI:** FastAPI WebSocket 서버 구현, YOLO11 모델 연동 및 실시간 웹캠 추론 스레드/Throttle 제어
- **Frontend:** React + TypeScript 기반 Z-Index 아바타 씬 레이어링 엔진 및 Glassmorphism UI 설계
---

## 🛠️ 기술 스택 (Tech Stack)

### Frontend
- **Framework & Language:** React 19, TypeScript, Vite
- **Styling:** Custom CSS (Glassmorphism & Neon Theme, CSS Keyframe Animations)
- **Communication:** Native WebSocket Client

### Backend & AI
- **Framework:** FastAPI, Uvicorn
- **AI / Computer Vision:** Ultralytics YOLO11 (`yolo11n.pt`), OpenCV (`cv2`)
- **Protocol:** WebSocket (Real-time Broadcast)

### Tooling & Monorepo
- **Package Manager:** npm (Concurrently 기반 멀티 프로세스 오케스트레이션)
- **Version Control:** Git, GitHub

---

## 🏗️ 시스템 아키텍처 및 작동 구조

```
[ 웹캠 영상 스트림 (Local Webcam) ]
                │
                ▼
[ OpenCV + YOLO11 AI 추론 ] ──(객체/사물 라벨 추출)
                │
                ▼
[ FastAPI 백엔드 (Python) ] ──(WebSocket 브로드캐스팅 / 1초 Throttle 제어)
                │  ws://127.0.0.1:8000/ws
                ▼
[ React + TypeScript (Vite) ]
  ├── 🎭 Virtual Avatar Stage (Z-Index 기반 깊이감 있는 사물 조합 합성)
  ├── 🔍 Real-time Detection Badges (현재 인식된 사물 목록)
  └── 📋 History Log (타임스탬프 기반 감지 기록)
```

---
### 🎯 핵심 씬 합성(Layering) 메커니즘
- **Layer 1 (배경/뒤쪽, `z-index: 1`)**: 의자(`🪑`), 침대(`🛏️`), 우산(`☂️`) 등
- **Layer 2 (캐릭터 본체, `z-index: 2`)**: 사용자 실루엣(`👤`)
- **Layer 3 (전면 소품/반려동물, `z-index: 3`)**: 손에 든 컵(`🥤`), 스마트폰(`📱`), 가위(`✂️`), 노트북(`💻`), 강아지/고양이(`🐶`/`🐱`) 등

---

## 🚀 추후 발전 및 활용 가능성

### 1. 🎙️ 경량 버튜버(VTuber) & 라이브 스트리밍 오버레이
- 고가의 모션 캡처 장비나 페이셜 트래킹 프로그램 없이도, OBS 브라우저 소스로 띄워 **"물 마시기, 폰 보기, 의자에 앉기, 작업하기"** 등의 현실 행동을 방송 화면에 위트 있는 이모지 아바타로 실시간 송출 가능

### 2. 🎮 인터랙티브 웹 게임 & 메타버스 소품 상호작용
- 카메라 앞에 실제 물건(특정 도구, 카드, 장난감)을 제시하면 가상 인벤토리에 장착되거나 퀘스트가 클리어되는 물리 연동 인터랙션 확장

### 3. 📊 홈 트레이닝 & 일상 루틴 트래커
- 덤벨, 요가매트, 책, 텀블러 등 특정 활동 사물의 노출 시간을 측정해 일상 루틴과 건강 데이터를 시각화하는 대시보드로 발전

---

## 💻 실행 방법 (Getting Started)

### 1. 사전 요구사항 (Prerequisites)
- **Node.js 18+** & npm
- **Python 3.10+**
- 웹캠(카메라)이 연결된 PC

---

### 2. 프로젝트 클론 및 의존성 설치

```
# 1) 저장소 클론 (Clone Repository)
git clone [https://github.com/Kim-yebin/cammoji_project.git](https://github.com/Kim-yebin/cammoji_project.git)
cd cammoji_project

# 2) Node 패키지 설치 (루트 및 프론트엔드)
npm install
cd frontend && npm install && cd ..

# 3) Python 가상환경 생성 및 활성화
python -m venv .venv

# Windows (PowerShell / CMD)
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 4) 백엔드 의존성 설치
pip install -r backend/requirements.txt
```

---

### 3. 원클릭 동시 실행 (Run Project)

루트 디렉터리에서 아래 명령어를 실행하면 FastAPI 백엔드(카메라+YOLO)와 React 프론트엔드(Vite)가 동시에 실행됩니다.
```
npm run dev
```
- 브라우저 대시보드: http://localhost:5173 접속
- 프로그램 종료: OpenCV 카메라 창이 활성화된 상태에서 키보드 q를 누르면 백엔드와 프론트엔드 프로세스가 모두 안전하게 동시 종료됩니다.
