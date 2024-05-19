from fastapi import APIRouter
from .securities import securities_router
from .equity_options import options_router

aggregated_router = APIRouter()
aggregated_router.include_router(securities_router, tags=["securities"])
aggregated_router.include_router(options_router, tags=["equity-options"])