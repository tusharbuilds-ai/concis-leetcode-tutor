from services.service_db.db import firebase_conn
from services.service_otp.OTP import otp_generater
from services.service_in_memory.inmemory import redis_con
from services.service_email.email_service import email_service
from core.LogManager import log

class UserService:
    def __init__(self):
        self.conn = firebase_conn
        self.in_memeory_store = redis_con


    def create_new_user(self,payload:str):
        log.debug(f"Received payload -> {payload}")
        
        safe_payload = payload.replace(".","_")

        user = firebase_conn.users_ref.child(safe_payload).get()

        if user is None:
            firebase_conn.users_ref.child(safe_payload).set({
                "email":safe_payload
            })


        log.debug("Using the OTP generater service...")
        otp = otp_generater.generate_otp(6)

        try:
            email_service.send_otp(payload,otp)
            log.debug("Adding the otp with expiry redis")
            self.in_memeory_store.set_expiry_based_key_value(payload,otp)
        except Exception as RedisException:
            log.exception(f"Exception while setting redis key | {RedisException}")

            return{
                "status":500,
                "message":"Can not process you request right now. Try again layer"
            }

        return{
            "status":200,
            "message":f"Received email -> {payload}",
            "generated_otp":f"OTP: {otp}"
        }




user_service = UserService()