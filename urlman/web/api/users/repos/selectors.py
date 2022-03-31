from typing import List, Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from urlman.db.dependencies import get_db_session
from urlman.db.models import UserModel
from urlman.settings import settings
from urlman.web.api.auth import jwt_auth
from urlman.web.api.users.exceptions import (
    UserCredentialsException,
    UserNotProvidedException,
)


async def get_user_by_id(*, user_id: str, session: AsyncSession) -> Optional[UserModel]:
    """Get user by id(UUID) from db."""
    stmt = (
        select(UserModel)
        .where(
            UserModel.id == user_id,
        )
        .options(
            joinedload(UserModel.urls),
        )
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_username(
    *,
    username: str,
    session: AsyncSession,
) -> Optional[UserModel]:
    """Get user by username from db."""
    stmt = select(UserModel).where(UserModel.username == username)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_users(*, session: AsyncSession) -> List[UserModel]:
    """Get all active user."""
    stmt = (
        select(UserModel)
        .where(
            UserModel.is_deleted == False,
        )
        .order_by(
            UserModel.created_at,
        )
    )
    result = await session.execute(stmt)
    return result.scalars().fetchall()


async def get_all_users(*, session: AsyncSession) -> List[UserModel]:
    """Get all users from db."""
    stmt = select(UserModel).order_by(UserModel.created_at)
    result = await session.execute(stmt)
    return result.scalars().fetchall()


async def get_current_user(
    *,
    token: HTTPAuthorizationCredentials = Depends(settings.auth_scheme),
    session: AsyncSession = Depends(get_db_session),
) -> Optional[UserModel]:
    """Getting the current user."""
    try:
        username = jwt_auth.decode_token(token=token.credentials)
    except Exception:
        raise UserNotProvidedException()
    user = await get_user_by_username(username=username, session=session)
    if user is None:
        raise UserCredentialsException()
    return user
