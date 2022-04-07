from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from urlman.db.models.user import UserModel
from urlman.services.hashing import hash_password, verify_password
from urlman.web.api.users.exceptions import (
    UserNotFoundException,
    UserPasswordMismatchException,
)
from urlman.web.api.users.repos.selectors import get_user_by_id
from urlman.web.api.users.schemas import UserChangePassword, UserIn, UserUpdate


async def register_user(*, user: UserIn, session: AsyncSession) -> UserModel:
    """Create new user."""
    hashed_password = hash_password(user.password)
    user = UserModel(
        username=user.username,
        email=user.email,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(
    *,
    user_id: str,
    data: UserUpdate,
    session: AsyncSession,
) -> Optional[UserModel]:
    """Update user."""
    user = await get_user_by_id(
        session=session,
        user_id=user_id,
    )
    if user is None:
        raise UserNotFoundException()

    updated_data = data.dict(exclude_none=True, exclude_unset=True)
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


async def soft_delete_user(
    *,
    user_id: str,
    session: AsyncSession,
) -> Optional[UserModel]:
    """Change is_deleted to True."""
    user = await get_user_by_id(
        session=session,
        user_id=user_id,
    )
    if user is None:
        raise UserNotFoundException()

    user.is_deleted = True
    user.deleted_at = func.now()
    await session.commit()
    return user


async def delete_user(
    *,
    user_id: str,
    session: AsyncSession,
) -> None:
    """Delete user from db."""
    user = await get_user_by_id(
        session=session,
        user_id=user_id,
    )
    if user is None:
        raise UserNotFoundException()
    await session.delete(user)
    await session.commit()


async def change_user_password(
    *,
    user: UserModel,
    creds: UserChangePassword,
    session: AsyncSession,
) -> None:
    """Change user password."""
    creds_data = creds.dict(exclude_none=True, exclude_unset=True)
    if verify_password(
        db_password=user.password,
        verifiable_password=creds_data.pop("password"),
    ):
        user.password = hash_password(creds_data.pop("new_password"))
        await session.commit()
    else:
        raise UserPasswordMismatchException()
