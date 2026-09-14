from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.help_requests.router import router as help_requests_router
from app.modules.agents.router import router as agents_router
from app.modules.campaigns.router import router as campaigns_router
from app.modules.media.router import router as media_router
from app.modules.moderation.router import router as moderation_router
from app.modules.donations.router import router as donations_router
from app.modules.payments.router import router as payments_router
from app.modules.payouts.router import router as payouts_router
from app.modules.reports.router import router as reports_router
from app.modules.disputes.router import router as disputes_router
from app.modules.notifications.router import router as notifications_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(help_requests_router)
api_router.include_router(agents_router)
api_router.include_router(campaigns_router)
api_router.include_router(media_router)
api_router.include_router(moderation_router)
api_router.include_router(donations_router)
api_router.include_router(payments_router)
api_router.include_router(payouts_router)
api_router.include_router(reports_router)
api_router.include_router(disputes_router)
api_router.include_router(notifications_router)
