from fastapi import APIRouter, Request
from schemas.chat_schema import ChatSchem
from core.RateLimiter import limiter
from core.LogManager import log
from services.service_push_to_queue.psuh_to_queue import push_user_queue
from managers.session_manager.sessions import session_manager
chat_router = APIRouter()


@limiter.limit("20/minute")
@chat_router.post("")
def chat(request:Request,
         payload:ChatSchem):
    log.info(f"User request recieved -> {payload}")
    #session_manager.ensure_session(payload.email,payload.session_id)
    result = push_user_queue.push_to_worker_queue(payload)
    return{
        "result":result
    }
   