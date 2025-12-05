from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from recorder_manager import RecorderManager
from websocket_hub import WebSocketHub

app = FastAPI()
hub = WebSocketHub()
recorder = RecorderManager(hub)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/events")
async def event_socket(websocket: WebSocket):
    await hub.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        hub.disconnect(websocket)

@app.post("/start")
async def start_recording():
    recorder.start()
    return {"status": "recording_started"}

@app.post("/stop")
async def stop_recording():
    recorder.stop()
    return {"status": "recording_stopped"}

@app.get("/steps")
async def get_steps():
    return recorder.get_steps()

@app.post("/export")
async def export_yaml():
    return {"file": recorder.export_yaml()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)