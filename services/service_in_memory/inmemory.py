import json
from redis import Redis
from core.LogManager import log
from schemas.chat_schema import ChatSchem
from schemas.logout_schema import LogoutSchema
from fastapi import HTTPException
import os
from dotenv import load_dotenv


load_dotenv()

class ServiceInMemory:
    def __init__(self):
        self.redis_conn = Redis(
            host=os.environ["REDIS_HOST"],
            port=os.environ["REDIS_PORT"],
            password= os.environ["REDIS_PASSWORD"]
        )
    

    def logout_cleanup(self,payload:LogoutSchema):
        result = self.redis_conn.delete(
            f"session:{payload.email}"
        )
        
        log.debug(f"Log out clean up session {payload.session_id} | {result}")

        return result


    def verify_session(self,email:str,session_id:str):
        result = self.redis_conn.get(
            f"session:{email}"
        )

        if result:
            s = result.decode("utf-8")
            log.debug(f"Actual session {s} session submited by user {session_id}")
            if s == session_id:
                return True
            else:
                raise HTTPException(
                    status_code=401,
                    detail="UNAUTHORIZED"
                )

    def check_current_session(self,email:str):
        result = self.redis_conn.get(
            f"session:{email}"
        )

        log.debug(f"Current session info -> {result}")   

        if result:
            session_id = result.decode("utf-8")
            return {
                "status":True,
                "session_id":session_id
            }
        return False

    def make_new_session(self,email:str,session:str):
        result = self.redis_conn.set(
            f"session:{email}",
            session
        )
        log.debug(f"Redis result -> {result}")
        return result


    def set_expiry_based_key_value(self,email:str,otp:str):
        self.redis_conn.setex(
            f"otp:{email}",
            300,
            otp,
        )
    
    def check_otp(self,email:str,user_submitted_otp:int):
        log.debug(f"Running command | get otp:{email}")
        result = self.redis_conn.get(
            f"otp:{email}"
        )    
        log.debug(f"Result from Redis | {result}")
        if user_submitted_otp == result.decode("utf-8"):
            return True
        return False

    def push_to_agent_work(self,payload:ChatSchem):
        processed_payload = payload.model_dump_json()

        result = self.redis_conn.lpush(
            "agent_worker_queue",
             processed_payload
         )
        
        if result != -1:
            return True
        else:
            return False
   
    def pull_for_agent_work_queue(self):

        item = self.redis_conn.brpop(
            "agent_worker_queue"
        )

        query, raw_payload = item

        payload = json.loads(raw_payload.decode())

        return payload

    def publish_agent_response(
            self,
            session_id:str,
            response:str
    ):
        payload={
            "session_id":session_id,
            "response":response
        }
        try:
            self.redis_conn.publish(
                "agent_response",
                json.dumps(payload)
            )
            log.debug(f"Response for session-id {session_id} published")
            
        
        except Exception as RedisPublishError:
            log.warn(f"Response for session-id {session_id}  can not be published due to {RedisPublishError}")


redis_con = ServiceInMemory()