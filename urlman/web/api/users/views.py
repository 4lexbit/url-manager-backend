from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage, paginate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from urlman.db.dependencies import get_db_session
from urlman.web.api.users.repos.selectors import get_user_by_id, get_users
from urlman.web.api.users.repos.services import (
    delete_user,
    register_user,
    soft_delete_user,
    update_user,
)
from urlman.web.api.users.schemas import UserIn, UserOut, UserOutExtended, UserUpdate

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=201)
async def create_user(
    user: UserIn,
    session: AsyncSession = Depends(get_db_session),
):
    """Create new User."""
    try:
        user = await register_user(session, user)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return user


@router.get("/{user_id}", response_model=UserOutExtended, status_code=200)
async def get_single_user(
    user_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    """Get single User."""
    try:
        user = await get_user_by_id(session, user_id)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("", response_model=LimitOffsetPage[UserOut], status_code=200)
async def get_list_users(
    session: AsyncSession = Depends(get_db_session),
):
    """Get list of undeleted active Users."""
    users = await get_users(
        session=session,
    )

    return paginate(users)


@router.patch("/{user_id}", response_model=UserOut, status_code=200)
async def update_single_user(
    user_id: str,
    data: UserUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    """Update User info."""
    try:
        user = await update_user(session=session, user_id=user_id, data=data)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}/soft_delete", status_code=204)
async def delete_user_soft(
    user_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    """Soft delete user."""
    try:
        user = await soft_delete_user(
            session=session,
            user_id=user_id,
        )
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=200)
async def delete_user_hard(
    user_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    """Delete User."""
    try:
        user = await delete_user(
            session=session,
            user_id=user_id,
        )
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")


# @router.get("/me", status_code=200)
# async def profile(
#     session: AsyncSession = Depends(get_db_session),
# ):
#     """Get current User profile."""
#     pass
#
# @router.patch("/change_password", status_code=200)
# async def update_user_password(
#     user_credentials: UserChangePassword,
#     session: AsyncSession = Depends(get_db_session),
# ):
#     """Change current user password."""
#     pass
