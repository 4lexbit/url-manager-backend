from typing import Optional

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from urlman.db.models.transition import TransitionModel
from urlman.db.models.urls import UrlModel


async def create_transition(
    *,
    client_ip: Optional[str],
    url: UrlModel,
    session: AsyncSession,
) -> Optional[TransitionModel]:
    """Create url transition."""
    transition = TransitionModel(
        ip=client_ip,
        check_time=func.now(),
        url=url,
        url_id=url.id,
    )
    session.add(transition)
    await session.commit()
    return transition
