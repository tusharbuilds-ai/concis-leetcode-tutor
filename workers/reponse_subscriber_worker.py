import json
import asyncio
from services.service_in_memory.inmemory import redis_con
from managers.websocket_manager.websocket_manager import websock_manager
from core.LogManager import log

async def listen_agent_response():
    pubsub = redis_con.redis_conn.pubsub()

    pubsub.subscribe(
        "agent_response"
    )

    while True:
        message = pubsub.get_message()

        if message is None:
            await asyncio.sleep(0.1)
            continue

        log.debug(f"Redis Message {message}")

        if message["type"] == "message":
            
            payload = json.loads(message["data"])

            log.debug(f"Subscriber got {payload}")

            session_id = payload["session_id"]
            response = payload["response"]

            try:
                await websock_manager.send_message(
                    session_id=session_id,
                    message=response
                ) 
                log.debug("Message sent back to the user")
            except Exception as WebSocketException:
                log.warn(f"Websocket error in subscriber {WebSocketException}")
        continue   