## 🎟️ Bézier Cutline Generator

티켓 이미지에 **랜덤 Bézier 곡선으로 절취선(cutline)** 을 생성하는 실험용 프로젝트입니다.  

실행 방식에 따라:

- 메모리에서만 생성/미리보기(파일 저장 X)
- 이미지 + JSON 파일로 저장(옵션)

두 가지로 사용할 수 있습니다.

---

### 📂 Project Structure
```
bezier_creator/
├── bezier_create.py         # 메인 스크립트 (메모리/미리보기용, 저장 X)
├── bezier_create.py # 메인 스크립트 (컷라인 생성)
├── output/ # 생성된 이미지 및 JSON 저장 폴더
│     ├── ticket_cutline_1.png # 출력 예시
│     └── ticket_cutline_1.json
│
├── ticket.png # 원본 티켓 이미지 (예시)
└── .gitignore 
```

---

### 🚀 How to Use

#### 1. 메모리/미리보기 전용 실행 (bezier_create.py)
파일을 저장하지 않고, 이미지 + 좌표 정보만 메모리에서 사용하고 싶을 때:
```bash
cd /Users/bell/Desktop/bezier_creator  # 예시

python bezier_create.py
```
- 동작:
  - ticket.png를 불러와서 랜덤 Bézier 절취선을 그림
  - 결과 이미지:
    - matplotlib 창으로 한 번 보여줌 (미리보기용)
    - 메타데이터:
      - 터미널에 JSON 형태로 출력됨
        (예: `curve_points`, `base_x`, `ticket_y_range` 등)

이 버전은 실무 서비스 코드에 연동하기 좋은 형태이다.

#### 2. 파일 저장용 실행 (bezier_create_saved.py)
절취선이 적용된 이미지를 파일로 계속 쌓고 싶을 때:
```bash
cd /Users/bell/Desktop/bezier_creator   # 예시

python bezier_create_saved.py
```

- 동작:
  - output/ 폴더가 없으면 자동 생성
  - 실행할 때마다:
    - `output/ticket_cutline_1.png`, `ticket_cutline_2.png`, … 순서대로 저장
    - 같은 이름의 .json 파일도 함께 저장
      (절취선 곡선 좌표 및 관련 메타데이터 포함)

- 예시: 
| 파일                             | 설명                     |
| ------------------------------ | ---------------------- |
| `output/ticket_cutline_1.png`  | Bézier 절취선이 적용된 티켓 이미지 |
| `output/ticket_cutline_1.json` | 절취선 좌표 및 메타데이터(JSON)   |


### 🧠 Internal Action Summary 
- 4개의 제어점(P0, P1, P2, P3)으로 3차 Bézier 곡선 생성
- 곡선 상의 점들을 따라 점선(dashed line) 형태의 절취선 렌더링
- 랜덤 요소:
  - X축 중심 위치 (약간의 랜덤 오프셋)
  - 중간 제어점(P1, P2)의 X 좌표가 약간 흔들리도록 설정 → 자연스럽게 구부러진 절취선


---

### ✨ Features
- 랜덤 Bézier 기반 자연스러운 곡선 절취선
- OpenCV 기반 이미지 처리
- 메타데이터(JSON)를 통해:
  - 절취선 좌표를 서버/클라이언트 로직에서 재활용 가능
- 실무 서비스에 연동할 땐:
  - `bezier_create.py`의 generate_cutline() 함수를 그대로 가져다 쓰면 됨
  - “파일은 저장하지 않고, 메모리만 쓰는” 구조라 API에 붙이기 좋음