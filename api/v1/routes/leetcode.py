from fastapi import APIRouter,Request
from services.service_leetcode.leetcode import leetcode_service
from core.RateLimiter import limiter

leetcode_router = APIRouter()

@limiter.limit("10/minute")
@leetcode_router.get("")
def get_problems(request:Request):
    return (
        leetcode_service.get_problems()
    )