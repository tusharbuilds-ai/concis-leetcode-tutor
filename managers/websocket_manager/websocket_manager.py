from fastapi import WebSocket
from core.LogManager import log

class WebSocketManager:
    def __init__(self):
        self.active_connections:dict = {}
    
        log.debug(f"Size of active connections : {self.active_connections.values}")

    async def connect(self,session_id:str,websocket:WebSocket):
        try:
            self.active_connections[session_id]=websocket
            log.debug(self.active_connections.items())
        except Exception as e:
            log.error(f"{e}")
    async def disconnect(self,session_id:str):
        self.active_connections.pop(session_id),None
    
    async def send_message(self,session_id:str,message:str):
        ws = self.active_connections[session_id]
        await ws.send_text(message)


websock_manager = WebSocketManager()