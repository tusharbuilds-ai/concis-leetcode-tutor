from fastapi import APIRouter
from schemas.logout_schema import LogoutSchema
from services.service_logout.logout import logout_clean
from core.LogManager import log

logout_router = APIRouter()

@logout_router.post("")
def logout(payload:LogoutSchema):
     result = logout_clean.perform_logout_cleanup(payload)
     log.debug(result)