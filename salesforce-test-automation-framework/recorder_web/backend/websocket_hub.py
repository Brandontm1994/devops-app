class WebSocketHub:

    def __init__(self):
        self.active = set()

    async def connect(self, websocket):
        await websocket.accept()
        self.active.add(websocket)

    def disconnect(self, websocket):
        if websocket in self.active:
            self.active.remove(websocket)

    async def broadcast(self, message: str):
        dead = []
        for ws in self.active:
            try:
                await ws.send_text(message)
            except:
                dead.append(ws)
        for ws in dead:
            self.active.remove(ws)