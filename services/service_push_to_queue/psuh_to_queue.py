from services.service_in_memory.inmemory import redis_con
from core.LogManager import log
from schemas.chat_schema import ChatSchem


class PushToQueueService:
    def __init__(self):
        self.redis_conn = redis_con

    

    def push_to_worker_queue(self,payload:ChatSchem):
        log.debug(f"Payload recieved by push_to_worker_queuer : {payload}")

        log.debug("Pushing to worker queue....")

        result = redis_con.push_to_agent_work(payload)

        if result:
            return{
                "status":200,
                "message":"Request pushed to queue."
            }
        
        return{
                "status":500,
                "message":"can not be fulfilled."
            }


push_user_queue = PushToQueueService()