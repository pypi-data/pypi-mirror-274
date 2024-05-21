from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from fastapi import APIRouter
from ..log_streaming.log_streaming import get_log_stream_html


def get_log_stream_views_router(logger, router: APIRouter= None):
    if not router:
        router = APIRouter(include_in_schema=False)
    
    @router.get("/logs")
    async def get():
        html = get_log_stream_html()
        return HTMLResponse(html)

    @router.websocket("/logs")
    async def log_stream(websocket: WebSocket):
        await logger.settings.stream.connect(websocket)
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            logger.settings.stream.disconnect(websocket)
    
    return router
    
