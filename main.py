import os
import asyncio
import threading
import json
import time
import cv2
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO

app = FastAPI()

# 🔥 정적 파일(CSS, JS, 이미지 등) 제공을 위한 static 디렉터리 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")

# 1. 모델 로드
model = YOLO("yolo11n.pt")

# 2. COCO 80개 사물 전체 이모지 매핑
COCO_EMOJI_MAP = {
    "person": "👤", "bicycle": "🚲", "car": "🚗", "motorcycle": "🏍️",
    "airplane": "✈️", "bus": "🚌", "train": "🚆", "truck": "🚚", "boat": "🛥️",
    "traffic light": "🚦", "fire hydrant": "🧯", "stop sign": "🛑",
    "parking meter": "🅿️", "bench": "🪑", "bird": "🐦", "cat": "🐱",
    "dog": "🐶", "horse": "🐴", "sheep": "🐑", "cow": "🐮", "elephant": "🐘",
    "bear": "🐻", "zebra": "🦓", "giraffe": "🦒", "backpack": "🎒",
    "umbrella": "☂️", "handbag": "👜", "tie": "👔", "suitcase": "🧳",
    "frisbee": "🥏", "skis": "🎿", "snowboard": "🏂", "sports ball": "⚽",
    "kite": "🪁", "baseball bat": "🏏", "baseball glove": "🧤",
    "skateboard": "🛹", "surfboard": "🏄", "tennis racket": "🎾",
    "bottle": "🍾", "wine glass": "🍷", "cup": "☕", "fork": "🍴",
    "knife": "🔪", "spoon": "🥄", "bowl": "🥣", "banana": "🍌",
    "apple": "🍎", "sandwich": "🥪", "orange": "🍊", "broccoli": "🥦",
    "carrot": "🥕", "hot dog": "🌭", "pizza": "🍕", "donut": "🍩",
    "cake": "🎂", "chair": "🪑", "couch": "🛋️", "potted plant": "🪴",
    "bed": "🛏️", "dining table": "🍽️", "toilet": "🚽", "tv": "📺",
    "laptop": "💻", "mouse": "🖱️", "remote": "📱", "keyboard": "⌨️",
    "cell phone": "📱", "microwave": "📻", "oven": "🍳", "toaster": "🍞",
    "sink": "🚰", "refrigerator": "🧊", "book": "📖", "clock": "⏰",
    "vase": "🏺", "scissors": "✂️", "teddy bear": "🧸", "hair drier": "💨",
    "toothbrush": "🪥"
}

active_websockets: list[WebSocket] = []
main_loop = None

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        active_websockets.remove(websocket)

async def broadcast_detection(detected_classes: list[str], detected_emojis: list[str]):
    if active_websockets:
        message = json.dumps({
            "classes": detected_classes,
            "emojis": detected_emojis
        })
        for ws in active_websockets:
            try:
                await ws.send_text(message)
            except Exception:
                pass

def camera_loop():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ 카메라를 열 수 없습니다.")
        os._exit(1)

    print("🚀 캠모지 카메라 시작 (카메라 창에서 'q' 누르면 프로그램 완전 종료)")
    
    last_update_time = time.time()
    UPDATE_INTERVAL = 1.0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=0.45, verbose=False)
        detected_classes = []
        detected_emojis = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                class_name = model.names[cls_id]
                conf = float(box.conf[0])

                detected_classes.append(class_name)
                emoji_text = COCO_EMOJI_MAP.get(class_name, "📦")
                detected_emojis.append(emoji_text)

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, max(y1 - 10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        unique_classes = sorted(list(set(detected_classes)))
        unique_emojis = sorted(list(set(detected_emojis)))
        current_time = time.time()

        if current_time - last_update_time >= UPDATE_INTERVAL:
            current_str = " ".join(unique_emojis) if unique_emojis else "사물 없음"
            print(f"[{time.strftime('%H:%M:%S')}] 현재 인식: {current_str}")

            if main_loop and main_loop.is_running():
                asyncio.run_coroutine_threadsafe(
                    broadcast_detection(unique_classes, unique_emojis), main_loop
                )

            last_update_time = current_time

        cv2.imshow("Cammoji Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("👋 프로그램을 완전히 종료합니다...")
            break

    cap.release()
    cv2.destroyAllWindows()
    os._exit(0)

@app.on_event("startup")
async def startup_event():
    global main_loop
    main_loop = asyncio.get_event_loop()
    cam_thread = threading.Thread(target=camera_loop, daemon=True)
    cam_thread.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)