import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO

# 1. YOLO11 Nano 모델 로드
model = YOLO("yolo11n.pt")

# 2. COCO 80개 사물 전체 이모지 매핑
COCO_EMOJI_MAP = {
    "person": "👤 사람",
    "bicycle": "🚲 자전거",
    "car": "🚗 자동차",
    "motorcycle": "🏍️ 오토바이",
    "airplane": "✈️ 비행기",
    "bus": "🚌 버스",
    "train": "🚆 기차",
    "truck": "🚚 트럭",
    "boat": "🛥️ 보트",
    "traffic light": "🚦 신호등",
    "fire hydrant": "🧯 소화전",
    "stop sign": "🛑 정지 표지판",
    "parking meter": "🅿️ 주차 요금기",
    "bench": "🪑 벤치",
    "bird": "🐦 새",
    "cat": "🐱 고양이",
    "dog": "🐶 강아지",
    "horse": "🐴 말",
    "sheep": "🐑 양",
    "cow": "🐮 소",
    "elephant": "🐘 코끼리",
    "bear": "🐻 곰",
    "zebra": "🦓 얼룩말",
    "giraffe": "🦒 기린",
    "backpack": "🎒 가방",
    "umbrella": "☂️ 우산",
    "handbag": "👜 핸드백",
    "tie": "👔 넥타이",
    "suitcase": "🧳 캐리어",
    "frisbee": "🥏 프리스비",
    "skis": "🎿 스키",
    "snowboard": "🏂 스노보드",
    "sports ball": "⚽ 공",
    "kite": "🪁 연",
    "baseball bat": "🏏 야구 방망이",
    "baseball glove": "🧤 야구 글러브",
    "skateboard": "🛹 스케이트보드",
    "surfboard": "🏄 서핑보드",
    "tennis racket": "🎾 테니스 라켓",
    "bottle": "🍾 병",
    "wine glass": "🍷 와인잔",
    "cup": "☕ 컵",
    "fork": "🍴 포크",
    "knife": "🔪 나이프",
    "spoon": "🥄 숟가락",
    "bowl": "🥣 그릇",
    "banana": "🍌 바나나",
    "apple": "🍎 사과",
    "sandwich": "🥪 샌드위치",
    "orange": "🍊 오렌지",
    "broccoli": "🥦 브로콜리",
    "carrot": "🥕 당근",
    "hot dog": "🌭 핫도그",
    "pizza": "🍕 피자",
    "donut": "🍩 도넛",
    "cake": "🎂 케이크",
    "chair": "🪑 의자",
    "couch": "🛋️ 소파",
    "potted plant": "🪴 화분",
    "bed": "🛏️ 침대",
    "dining table": "🍽️ 식탁",
    "toilet": "🚽 변기",
    "tv": "📺 TV",
    "laptop": "💻 노트북",
    "mouse": "🖱️ 마우스",
    "remote": "📱 리모컨",
    "keyboard": "⌨️ 키보드",
    "cell phone": "📱 스마트폰",
    "microwave": "📻 전자레인지",
    "oven": "🍳 오븐",
    "toaster": "🍞 토스터",
    "sink": "🚰 싱크대",
    "refrigerator": "🧊 냉장고",
    "book": "📖 책",
    "clock": "⏰ 시계",
    "vase": "🏺 꽃병",
    "scissors": "✂️ 가위",
    "teddy bear": "🧸 곰인형",
    "hair drier": "💨 드라이기",
    "toothbrush": "🪥 칫솔"
}

# 3. 윈도우/맥/리눅스 한글 및 이모지 지원 폰트 로드
def get_korean_font(font_size=20):
    # 윈도우 기본 맑은 고딕
    win_font = "C:/Windows/Fonts/malgun.ttf"
    mac_font = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    
    if os.path.exists(win_font):
        return ImageFont.truetype(win_font, font_size)
    elif os.path.exists(mac_font):
        return ImageFont.truetype(mac_font, font_size)
    else:
        return ImageFont.load_default()

font = get_korean_font(22)

# 4. OpenCV 프레임 위에 한글/이모지 텍스트를 그리는 함수
def draw_emoji_text(image_np, text, pos, bg_color=(0, 255, 0), text_color=(0, 0, 0)):
    x, y = pos
    img_pil = Image.fromarray(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    # 텍스트 크기 계산
    bbox = draw.textbbox((x, y), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # 가독성을 위한 텍스트 배경 박스
    draw.rectangle([x, max(0, y - text_h - 6), x + text_w + 10, y + 4], fill=bg_color)
    # 한글 + 이모지 텍스트 렌더링
    draw.text((x + 5, max(0, y - text_h - 6)), text, font=font, fill=text_color)

    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

# 5. 웹캠 연결
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ 카메라를 열 수 없습니다.")
    exit()

print("🚀 캠모지(Cammoji) 실행 중... 종료하려면 카메라 창에서 'q'를 누르세요.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO 객체 탐지 수행
    results = model(frame, conf=0.4, verbose=False)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]
            conf = float(box.conf[0])

            # 매핑 딕셔너리에서 이모지 라벨 조회
            emoji_label = COCO_EMOJI_MAP.get(class_name, f"📦 {class_name}")
            display_text = f"{emoji_label} ({int(conf * 100)}%)"

            # 바운딩 박스 그리기
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # 박스 상단에 이모지 텍스트 렌더링
            frame = draw_emoji_text(frame, display_text, (x1, y1), bg_color=(0, 255, 0), text_color=(0, 0, 0))

    cv2.imshow("Cammoji", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()