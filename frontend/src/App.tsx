import { useEffect, useState, useRef } from "react";
import "./App.css";

interface DetectionPayload {
  classes: string[];
  emojis: string[];
}

interface LogEntry {
  id: number;
  emojis: string[];
  time: string;
}

const EMOJI_MAP: Record<string, string> = {
  person: "👤",
  bicycle: "🚲",
  car: "🚗",
  motorcycle: "🏍️",
  airplane: "✈️",
  bus: "🚌",
  train: "🚆",
  truck: "🚚",
  boat: "🛥️",
  "traffic light": "🚦",
  "fire hydrant": "🧯",
  "stop sign": "🛑",
  "parking meter": "🅿️",
  bench: "🪑",
  bird: "🐦",
  cat: "🐱",
  dog: "🐶",
  horse: "🐴",
  sheep: "🐑",
  cow: "🐮",
  elephant: "🐘",
  bear: "🐻",
  zebra: "🦓",
  giraffe: "🦒",
  backpack: "🎒",
  umbrella: "☂️",
  handbag: "👜",
  tie: "👔",
  suitcase: "🧳",
  frisbee: "🥏",
  skis: "🎿",
  snowboard: "🏂",
  "sports ball": "⚽",
  kite: "🪁",
  "baseball bat": "🏏",
  "baseball glove": "🧤",
  skateboard: "🛹",
  surfboard: "🏄",
  "tennis racket": "🎾",
  bottle: "🍾",
  "wine glass": "🍷",
  cup: "☕",
  fork: "🍴",
  knife: "🔪",
  spoon: "🥄",
  bowl: "🥣",
  banana: "🍌",
  apple: "🍎",
  sandwich: "🥪",
  orange: "🍊",
  broccoli: "🥦",
  carrot: "🥕",
  "hot dog": "🌭",
  pizza: "🍕",
  donut: "🍩",
  cake: "🎂",
  chair: "🪑",
  couch: "🛋️",
  "potted plant": "🪴",
  bed: "🛏️",
  "dining table": "🍽️",
  toilet: "🚽",
  tv: "📺",
  laptop: "💻",
  mouse: "🖱️",
  remote: "📱",
  keyboard: "⌨️",
  "cell phone": "📱",
  microwave: "📻",
  oven: "🍳",
  toaster: "🍞",
  sink: "🚰",
  refrigerator: "🧊",
  book: "📖",
  clock: "⏰",
  vase: "🏺",
  scissors: "✂️",
  "teddy bear": "🧸",
  "hair drier": "💨",
  toothbrush: "🪥",
};

const BACK_ITEMS: Record<string, string> = {
  chair: "🪑",
  couch: "🛋️",
  bench: "🪑",
  bed: "🛏️",
};

const PET_ITEMS: Record<string, string> = {
  dog: "🐶",
  cat: "🐱",
  bird: "🐦",
  "teddy bear": "🧸",
  horse: "🐴",
  sheep: "🐑",
  cow: "🐮",
  elephant: "🐘",
  bear: "🐻",
  zebra: "🦓",
  giraffe: "🦒",
  "potted plant": "🪴",
};

export default function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [classes, setClasses] = useState<string[]>([]);
  const [emojis, setEmojis] = useState<string[]>([]);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const lastKeyRef = useRef("");

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onopen = () => setIsConnected(true);
    ws.onclose = () => setIsConnected(false);

    ws.onmessage = (event) => {
      const data: DetectionPayload = JSON.parse(event.data);
      const incomingClasses = data.classes || [];
      const incomingEmojis = data.emojis || [];

      setClasses(incomingClasses);
      setEmojis(incomingEmojis);

      const currentKey = incomingClasses.slice().sort().join(",");
      if (incomingClasses.length > 0 && currentKey !== lastKeyRef.current) {
        lastKeyRef.current = currentKey;
        const newLog: LogEntry = {
          id: Date.now(),
          emojis: incomingEmojis,
          time: new Date().toLocaleTimeString(),
        };
        setLogs((prev) => [newLog, ...prev.slice(0, 19)]);
      }
    };

    return () => ws.close();
  }, []);

  const renderStage = () => {
    if (classes.length === 0) {
      return {
        content: (
          <div className="person-body" style={{ opacity: 0.4 }}>
            🫥
          </div>
        ),
        desc: "카메라에 사물을 비춰보세요",
      };
    }

    if (classes.includes("person")) {
      let backEmoji = "";
      let umbrellaEmoji = "";
      let petEmoji = "";
      let laptopEmoji = "";
      let leftHandEmoji = "";
      let rightHandEmoji = "";
      const actions: string[] = [];

      for (const [cls, emoji] of Object.entries(BACK_ITEMS)) {
        if (classes.includes(cls)) {
          backEmoji = emoji;
          actions.push(emoji);
          break;
        }
      }

      if (classes.includes("umbrella")) {
        umbrellaEmoji = "☂️";
        actions.push("☂️");
      }

      for (const [cls, emoji] of Object.entries(PET_ITEMS)) {
        if (classes.includes(cls)) {
          petEmoji = emoji;
          actions.push(emoji);
          break;
        }
      }

      if (classes.includes("laptop")) {
        laptopEmoji = "💻";
        actions.push("💻");
      }

      const heldCandidates = classes.filter(
        (c) =>
          c !== "person" &&
          !BACK_ITEMS[c] &&
          !PET_ITEMS[c] &&
          c !== "umbrella" &&
          c !== "laptop",
      );

      if (heldCandidates.length > 0) {
        leftHandEmoji = EMOJI_MAP[heldCandidates[0]] || "📦";
        actions.push(leftHandEmoji);

        if (heldCandidates.length > 1) {
          rightHandEmoji = EMOJI_MAP[heldCandidates[1]] || "📦";
          actions.push(rightHandEmoji);
        }
      }

      return {
        content: (
          <>
            {backEmoji && <div className="obj-back-chair">{backEmoji}</div>}
            {umbrellaEmoji && (
              <div className="obj-back-umbrella">{umbrellaEmoji}</div>
            )}
            <div className="person-body">👤</div>
            {leftHandEmoji && (
              <div className="obj-front-cup">{leftHandEmoji}</div>
            )}
            {rightHandEmoji && (
              <div className="obj-front-phone">{rightHandEmoji}</div>
            )}
            {laptopEmoji && (
              <div className="obj-front-laptop">{laptopEmoji}</div>
            )}
            {petEmoji && <div className="obj-side-pet">{petEmoji}</div>}
          </>
        ),
        desc:
          actions.length > 0 ? `사람 + ${actions.join(" ")}` : "사람 인식됨",
      };
    }

    const itemStr = emojis.slice(0, 3).join(" ");
    return {
      content: <div className="solo-item">{itemStr}</div>,
      desc: `사물 감지됨 (${emojis.join(" ")})`,
    };
  };

  const stage = renderStage();

  return (
    <>
      <header className="app-header">
        <h1 className="title">✨ Cammoji Stage</h1>
        <div className={`status-badge ${isConnected ? "connected" : ""}`}>
          <span className="status-dot" />
          <span>
            {isConnected
              ? "카메라 & 백엔드 실시간 연결됨"
              : "백엔드 연결 대기 중..."}
          </span>
        </div>
      </header>

      <main className="container">
        <div className="stage-card">
          <div className="stage-title">Cammoji Live Scene</div>
          <div className="avatar-scene">{stage.content}</div>
          <div className="scene-action-text">{stage.desc}</div>
        </div>

        <div className="card">
          <div className="card-header">🔍 현재 감지된 사물</div>
          <div className="detected-badges">
            {emojis.length === 0 ? (
              <span className="empty-text">인식된 사물이 없습니다.</span>
            ) : (
              emojis.map((e, idx) => (
                <span key={idx} className="badge">
                  {e}
                </span>
              ))
            )}
          </div>
        </div>

        <div className="card">
          <div className="card-header">📋 감지 히스토리 로그</div>
          <div className="log-box">
            {logs.length === 0 ? (
              <span className="empty-text">기록된 감지 내역이 없습니다.</span>
            ) : (
              logs.map((log) => (
                <div key={log.id} className="log-item">
                  <span>{log.emojis.join("  ")}</span>
                  <span className="log-time">{log.time}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </main>
    </>
  );
}
