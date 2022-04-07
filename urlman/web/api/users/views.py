from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage, paginate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from urlman.db.dependencies import get_db_session
from urlman.db.models import UserModel
from urlman.services.hashing import verify_password
from urlman.web.api.auth import jwt_auth
from urlman.web.api.auth.schemas import AccessToken
from urlman.web.api.users.exceptions import UserNotFoundException
from urlman.web.api.users.repos.selectors import (
    get_current_user,
    get_user_by_id,
    get_user_by_username,
    get_users,
)
from urlman.web.api.users.repos.services import (
    change_user_password,
    delete_user,
    register_user,
    soft_delete_user,
    update_user,
)
from urlman.web.api.users.schemas import (
    UserChangePassword,
    UserCredentials,
    UserExtended,
    UserIn,
    UserOut,
    UserUpdate,
)

router = APIRouter()


@router.get("/profile", response_model=UserExtended, status_code=200)
async def profile(
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Get current User profile."""
    return await get_user_by_id(
        user_id=current_user.id,
        session=session,
    )


@router.get("/{user_id}", response_model=UserExtended, status_code=200)
async def get_single_user(
    user_id: str,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Get single User."""
    try:
        user = await get_user_by_id(user_id=user_id, session=session)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    if user is None:
        raise UserNotFoundException()
    return user


@router.get("", response_model=LimitOffsetPage[UserOut], status_code=200)
async def get_list_users(
    session: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Get list of undeleted active Users."""
    users = await get_users(
        session=session,
    )

    return paginate(users)


@router.post("/register", response_model=UserOut, status_code=201)
async def create_user(
    user: UserIn,
    session: AsyncSession = Depends(get_db_session),
):
    """Create new User."""
    try:
        user = await register_user(user=user, session=session)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return user


@router.post("/login", status_code=200, response_model=AccessToken)
async def login(
    user_credentials: UserCredentials,
    session: AsyncSession = Depends(get_db_session),
):
    """Get User token."""
    try:
        user = await get_user_by_username(
            username=user_credentials.username,
            session=session,
        )
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    if user is None:
        raise UserNotFoundException()
    if not verify_password(
        db_password=user.password,
        verifiable_password=user_credentials.password,
    ):
        raise UserNotFoundException()
    access_token = jwt_auth.encode_token(username=user.username)
    return AccessToken(access_token=access_token)


@router.patch("/change_password", status_code=200)
async def change_password(
    user_credentials: UserChangePassword,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Change current user password."""
    try:
        await change_user_password(
            user=current_user,
            creds=user_credentials,
            session=session,
        )
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))


@router.patch("/{user_id}", response_model=UserOut, status_code=200)
async def update_single_user(
    user_id: str,
    data: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Update User info."""
    try:
        user = await update_user(
            user_id=user_id,
            data=data,
            session=session,
        )
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    if user is None:
        raise UserNotFoundException()
    return user


@router.patch("/{user_id}/soft_delete", status_code=204)
async def delete_user_soft(
    user_id: str,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Soft delete user."""
    try:
        await soft_delete_user(
            user_id=user_id,
            session=session,
        )
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))


@router.delete("/{user_id}", status_code=200)
async def delete_user_hard(
    user_id: str,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Delete User."""
    try:
        await delete_user(
            user_id=user_id,
            session=session,
        )
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
