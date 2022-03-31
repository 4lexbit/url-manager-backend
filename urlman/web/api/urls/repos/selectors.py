from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.requests import Request

from urlman.db.models import UrlModel
from urlman.db.models.user import UserModel


async def get_shorted_url_by_id(
    *,
    url_id: str,
    child: bool = False,
    session: AsyncSession,
) -> Optional[UrlModel]:
    """Get shorted url by id from db."""
    if child:
        stmt = select(UrlModel).where(
            UrlModel.id == url_id,
            UrlModel.is_deleted == False,
        )
    else:
        stmt = (
            select(UrlModel)
            .where(
                UrlModel.id == url_id,
                UrlModel.is_deleted == False,
            )
            .options(
                joinedload(UrlModel.transitions),
            )
        )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_url_by_shortcode(
    url_shortcode: str,
    session: AsyncSession,
) -> Optional[UrlModel]:
    """Get shorted url by shortcode from db."""
    stmt = select(UrlModel).where(
        UrlModel.short_code == url_shortcode,
        UrlModel.is_deleted == False,
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_list_shorted_urls(
    user: UserModel,
    session: AsyncSession,
) -> List[UrlModel]:
    """Get shorted urls of current user."""
    stmt = select(UrlModel).where(
        UrlModel.user == user,
        UrlModel.is_deleted == False,
    )
    result = await session.execute(stmt)
    return result.scalars().fetchall()


async def get_all_urls(session: AsyncSession) -> List[UrlModel]:
    """Get all shorted urls."""
    stmt = select(UrlModel).order_by(UrlModel.created_at)
    result = await session.execute(stmt)
    return result.scalars().fetchall()


async def get_client_ip(request: Request) -> str:
    """Get client ip address from request."""
    if "x-forwarded-for" in request.headers:
        client_ip = request.headers.get("x-forwarded-for")
    else:
        client_ip = request.client.host
    return client_ip
