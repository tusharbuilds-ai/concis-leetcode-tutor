import uuid
from core.LogManager import log
from services.service_in_memory.inmemory import redis_con

class SessionManager:
    def __init__(self):
        self.redis_conn = redis_con
        


    def ensure_session(self,semail:str,session:str):
        result = self.redis_conn.verify_session
        return result

    def create_new_session(self,email:str):
        result = self.redis_conn.check_current_session(email) 
        
        if result:
            log.debug("Session exist for the user...")
            return{
                "response":result,
                "message":"Session already exist for this user."
            }
        else:
            log.debug("Creating new session for the user")

            unique_session_id = uuid.uuid4()
            session_id = unique_session_id

            log.debug(f"Newly session -> {session_id}, created for {email}")
            result = self.redis_conn.make_new_session(email,str(session_id))
            if result:
                return {
                    "response":{
                        "status":True,
                        "session_id":str(session_id)
                    }
                }

        
session_manager = SessionManager()