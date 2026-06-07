import random
import string
from services.service_in_memory.inmemory import redis_con
from managers.session_manager.sessions import session_manager
from schemas.otp_auth_schema import OtpAuthSchema
from core.LogManager import log

class ServiceOTP:
    def generate_otp(self,length:int):
        chars = string.ascii_uppercase + string.digits
        return "".join(random.choices(chars,k=length))
    
    def authenticate_otp(self,payload:OtpAuthSchema):
        log.debug("Authenticating OTP...")
        log.debug(f"Payload received -> {payload}")
        
        result = redis_con.check_otp(
            email=payload['email'],
            user_submitted_otp=payload['otp']        
        )

        if result:
            log.debug(f"Email for session creation {payload['email']} ")
            session_detail = session_manager.create_new_session(
                email=payload['email']
            )
            return {
                "session_detail":session_detail
            }
        else:
            return{
                "message":"Cannot authenticate the OTP. Try again"
            }


otp_generater = ServiceOTP()