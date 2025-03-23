import json
import asyncio
import websockets
from typing import Dict, List

class UpbitWebSocket:
    def __init__(self):
        self.ws = None
        self.url = "wss://api.upbit.com/websocket/v1"
        self.subscribed_markets = []
    
    async def connect(self):
        self.ws = await websockets.connect(self.url)
        await self._subscribe_to_markets()
    
    async def disconnect(self):
        if self.ws:
            await self.ws.close()
    
    async def get_market_data(self) -> Dict:
        if not self.ws:
            raise ConnectionError("WebSocket not connected")
        
        try:
            message = await self.ws.recv()
            return json.loads(message)
        except Exception as e:
            logging.error(f"WebSocket error: {e}")
            return {}
    
    async def _subscribe_to_markets(self):
        subscribe_fmt = [
            {"ticket":"UNIQUE_TICKET"},
            {
                "type":"ticker",
                "codes":self.subscribed_markets
            }
        ]
        await self.ws.send(json.dumps(subscribe_fmt))