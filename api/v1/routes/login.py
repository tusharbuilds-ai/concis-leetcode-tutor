from fastapi import APIRouter
from core.LogManager import log
from services.service_users.users import user_service
from schemas.login_schema import LoginSchema
from fastapi import Request
from core.RateLimiter import limiter

login_router = APIRouter()


@login_router.post("")
@limiter.limit("5/minute")
def login(
   request:Request,
   payload:LoginSchema
   ):
   log.debug(f"Sending paylaod to user service - > {payload.email}")
   result = user_service.create_new_user(payload=payload.email)
   log.debug(f"Received result from user service -> {result}")
   return result