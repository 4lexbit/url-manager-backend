from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from urlman.db.models.user import UserModel


async def get_user_by_id(session: AsyncSession, user_id: str):
    """Get user by id(UUID) from db."""
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_username(session: AsyncSession, username: str):
    """Get user by username from db."""
    stmt = select(UserModel).where(UserModel.username == username)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_users(session: AsyncSession):
    """Get all active user."""
    stmt = (
        select(UserModel)
        .where(
            UserModel.is_deleted == False,
            UserModel.is_active == True,
        )
        .order_by(
            UserModel.created_at,
        )
    )
    result = await session.execute(stmt)
    return result.scalars().fetchall()


async def get_all_users(session: AsyncSession):
    """Get all users from db."""
    stmt = select(UserModel).order_by(UserModel.created_at)
    result = await session.execute(stmt)
    return result.scalars().fetchall()
