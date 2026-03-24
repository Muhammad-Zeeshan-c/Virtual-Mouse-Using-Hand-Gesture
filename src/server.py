from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
import threading

class BackendServer:
    """
    FastAPI server to handle settings and status for the Virtual Mouse.
    """
    def __init__(self):
        self.app = FastAPI()
        self.settings = {
            "sensitivity": 5,
            "smoothing": 5,
            "enableMove": True,
            "enableClick": True,
            "enableRightClick": True,
            "enableScroll": True,
            "enableDrag": True
        }
        self.status = {
            "fps": 0,
            "gesture": "NONE",
            "hand_detected": False
        }
        
        # Enable CORS for React frontend
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self._setup_routes()

    def _setup_routes(self):
        @self.app.get("/settings")
        async def get_settings():
            return self.settings

        @self.app.post("/settings")
        async def update_settings(new_settings: dict):
            self.settings.update(new_settings)
            return self.settings

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            try:
                while True:
                    # Send current status every 100ms
                    await websocket.send_json({
                        "settings": self.settings,
                        "status": self.status
                    })
                    await asyncio.sleep(0.1)
            except Exception as e:
                print(f"WebSocket closed: {e}")

    def run(self):
        import uvicorn
        uvicorn.run(self.app, host="127.0.0.1", port=8000, log_level="error")

# Global instance for easy access
server_instance = BackendServer()

def start_server():
    server_instance.run()
