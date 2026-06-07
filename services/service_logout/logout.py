from services.service_in_memory.inmemory import redis_con
from schemas.logout_schema import LogoutSchema
from core.LogManager import log

class LogoutService:
    def perform_logout_cleanup(self,payload:LogoutSchema):
        try:
            result = redis_con.logout_cleanup(payload)
            log.debug(f"Result from log clean up service {result}")
            return result
        except Exception as LogoutCleanUPException:
            log.exception(f"Exception occured in log out clean up service {LogoutCleanUPException}")
            return{
                "status":False,
                "message":"Can't clean up.."
            }


logout_clean= LogoutService()