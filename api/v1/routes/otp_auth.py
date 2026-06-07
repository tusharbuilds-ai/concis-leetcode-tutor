from fastapi import APIRouter,Request
from services.service_otp.OTP import otp_generater
from core.LogManager import log
from schemas.otp_auth_schema import OtpAuthSchema
from core.RateLimiter import limiter

otp_auth_router = APIRouter()

@limiter.limit("1 per 5 minute")
@otp_auth_router.post("")
def authenticate_otp(
    request:Request,
    payload:OtpAuthSchema):
    payload = {
        "email":payload.email,
        "otp":payload.otp
    }
    log.debug("Sending OTP for authentication")
    result = otp_generater.authenticate_otp(payload)
    log.info(f"Result received from opt-auth | {result}")

    return{
        "result":result
    }