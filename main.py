import uvicorn
import os
import certifi
import asyncio
from api.v1.api import api_v1
from fastapi import FastAPI,WebSocket
from fastapi.middleware.cors import CORSMiddleware
from core.LogManager import log
from services.service_db.db import firebase_conn
from managers.websocket_manager.websocket_manager import websock_manager
from workers.reponse_subscriber_worker import listen_agent_response
from core.RateLimiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware

        


os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUEST_CA_BUNDLE"] = certifi.where()
os.environ["CURL_CA_BUNDLE"] = certifi.where()

app = FastAPI()

app.state.limiter = limiter


app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(
     SlowAPIMiddleware
)

app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=["*"],
)

app.include_router(api_v1,prefix="/api")

@app.on_event("startup")
async def startup():
    log.debug("Subscriber Started")
    asyncio.create_task(
        listen_agent_response()
    )

@app.get("/")
def health():
    log.info("Server is healty Up and Running !")
    return{
        "status":200,
        "message":"healthy"
    }



@app.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: str
):

    await websocket.accept()

    await websock_manager.connect(
        session_id,
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except Exception:

        await websock_manager.disconnect(
            session_id
        )





if __name__ == "__main__":
    uvicorn.run(
    app=app,
    host="0.0.0.0",
    port=8000,
    reload=True
)