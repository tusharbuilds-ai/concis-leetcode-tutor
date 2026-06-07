from fastapi import APIRouter
from api.v1.routes.login import login_router
from api.v1.routes.otp_auth import otp_auth_router
from api.v1.routes.chat import chat_router
from api.v1.routes.leetcode import leetcode_router
from api.v1.routes.logout import logout_router

api_v1 = APIRouter()

api_v1.include_router(login_router,prefix="/auth/otp-login")
api_v1.include_router(otp_auth_router,prefix="/auth/otp-auth")
api_v1.include_router(chat_router,prefix="/chat")
api_v1.include_router(leetcode_router,prefix="/leetcode/problems")
api_v1.include_router(logout_router,prefix="/logout")