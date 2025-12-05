import { useEffect, useState } from "react";

const WS_URL = "ws://localhost:5001/ws/events";
const API = "http://localhost:5001";

export function useRecorder() {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [events, setEvents] = useState<any[]>([]);
  const [steps, setSteps] = useState<any[]>([]);
  const [currentEvent, setCurrentEvent] = useState<any>(null);
  const [isRecording, setIsRecording] = useState(false);

  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    ws.onmessage = (msg) => {
      const evt = JSON.parse(msg.data);
      setCurrentEvent(evt);
      setEvents((e) => [...e, evt]);
      setSteps((s) => [...s, evt]);
    };
    setSocket(ws);

    return () => ws.close();
  }, []);

  async function startRecording() {
    setIsRecording(true);
    await fetch(`${API}/start`, { method: "POST" });
  }

  async function stopRecording() {
    setIsRecording(false);
    await fetch(`${API}/stop`, { method: "POST" });
  }

  async function exportYaml() {
    await fetch(`${API}/export`, { method: "POST" });
    alert("YAML exported on backend server.");
  }

  return {
    events,
    steps,
    currentEvent,
    isRecording,
    startRecording,
    stopRecording,
    exportYaml
  };
}