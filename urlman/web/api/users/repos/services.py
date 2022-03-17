from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from urlman.db.models.user import UserModel
from urlman.services.hashing import hash_password
from urlman.web.api.users.repos.selectors import get_user_by_id
from urlman.web.api.users.schemas import UserIn, UserUpdate


async def register_user(
    session: AsyncSession,
    user: UserIn,
) -> UserModel:
    """Create new user."""
    hashed_password = hash_password(user.password)
    user = UserModel(
        username=user.username,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    session.add(user)
    await session.commit()
    return user


async def update_user(
    session: AsyncSession,
    data: UserUpdate,
    user_id: str,
) -> Optional[UserModel]:
    """Update user."""
    user = await get_user_by_id(
        session=session,
        user_id=user_id,
    )
    updated_data = data.dict(exclude_none=True, exclude_unset=True)
    if user is None:
        return None

    hashed_password = hash_password(updated_data.get("password"))
    updated_data["password"] = hashed_password

    user_data = jsonable_encoder(
        user,
        exclude_none=True,
        exclude_unset=True,
    )

    for field in user_data:
        if field in updated_data:
            setattr(user, field, updated_data.get(field))
    await session.commit()
    return user


async def change_password(
    session: AsyncSession,
    user: UserModel,
) -> Optional[UserModel]:
    """Change user password."""


async def soft_delete_user(session: AsyncSession, user_id: str) -> UserModel:
    """Change is_deleted to True."""
    user = await get_user_by_id(
        session=session,
        user_id=user_id,
    )
    if user is None:
        return None
    user.is_deleted = False
    user.deleted_at = func.now()
    await session.commit()
    return user


async def delete_user(
    session: AsyncSession,
    user_id: str,
) -> Optional[UserModel]:
    """Delete user from db."""
    user = get_user_by_id(session, user_id)
    if user is None:
        return None
    await session.delete(user)
    await session.commit()
