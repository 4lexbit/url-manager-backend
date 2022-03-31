from typing import List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from urlman.db.models.transition import TransitionModel
from urlman.db.models.urls import UrlModel


async def get_transitions_by_url(
    *,
    url: UrlModel,
    session: AsyncSession,
) -> List[TransitionModel]:
    """Get transitions by url."""
    stmt = (
        select(TransitionModel)
        .where(
            TransitionModel.url == url,
        )
        .order_by(
            TransitionModel.check_time,
        )
    )
    result = await session.execute(stmt)
    return result.scalars().fetchall()


async def get_transitions_count(*, url: UrlModel, session: AsyncSession) -> int:
    """Get transitions count."""
    stmt = (
        select([func.count()])
        .select_from(
            TransitionModel,
        )
        .where(
            TransitionModel.url == url,
        )
    )
    result = await session.execute(stmt)
    return result.scalar()
