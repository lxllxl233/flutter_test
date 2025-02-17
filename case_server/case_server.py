from aiohttp import web
import json
import asyncio

class WebSocketServer:
    def __init__(self):
        self.app = web.Application()
        self.clients = set()
        self.setup_routes()

    def setup_routes(self):
        self.app.router.add_route('GET', '/ws', self.websocket_handler)
        self.app.router.add_route('POST', '/send', self.http_send_handler)
        self.app.router.add_static('/', path='./static', name='static')

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.clients.add(ws)

        try:
            async for msg in ws:
                # 处理客户端发来的消息（可选）
                if msg.type == web.WSMsgType.TEXT:
                    await self.broadcast(f"Client: {msg.data}")
        finally:
            self.clients.remove(ws)
        return ws

    async def http_send_handler(self, request):
        data = await request.json()
        message = data.get('message', '')
        await self.broadcast(message)
        return web.json_response({"status": "success"})

    async def broadcast(self, message):
        payload = json.dumps({"type": "broadcast", "data": message})
        for ws in self.clients.copy():
            if not ws.closed:
                await ws.send_str(payload)

if __name__ == '__main__':
    server = WebSocketServer()
    web.run_app(server.app, port=8080)