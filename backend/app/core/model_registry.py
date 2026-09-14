"""
Imports every SQLAlchemy model class so all relationships can be resolved
regardless of which module triggers the first database query.

Import this module once, early, in main.py before the app starts handling
requests. Add new model modules here as they are created.
"""

from app.modules.users.models import User, Role, Permission, UserRole, RolePermission  # noqa: F401
from app.modules.auth.models import RefreshToken  # noqa: F401
from app.modules.agents.models import AgentProfile, AgentVerification  # noqa: F401
from app.modules.help_requests.models import HelpRequest, HelpRequestAgent, HelpRequestEvent  # noqa: F401
from app.modules.media.models import Media  # noqa: F401
from app.modules.campaigns.models import CampaignCategory, Campaign, CampaignEvidence, CampaignUpdate  # noqa: F401
from app.modules.donations.models import Donation  # noqa: F401
from app.modules.payments.models import Payment  # noqa: F401
from app.modules.payouts.models import Payout  # noqa: F401
from app.modules.reports.models import Report, Review  # noqa: F401
from app.modules.disputes.models import Dispute  # noqa: F401
from app.modules.follows.models import Follow  # noqa: F401
from app.modules.notifications.models import Notification  # noqa: F401
from app.modules.audit.models import AuditLog  # noqa: F401
