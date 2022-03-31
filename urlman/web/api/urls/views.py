from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi_pagination import LimitOffsetPage, paginate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from urlman.db.dependencies import get_db_session
from urlman.db.models.user import UserModel
from urlman.web.api.transitions.repos.selectors import get_transitions_by_url
from urlman.web.api.transitions.repos.services import create_transition
from urlman.web.api.transitions.schemas import TransitionOut
from urlman.web.api.urls.exceptions import UrlNotFoundException
from urlman.web.api.urls.repos.selectors import (
    get_client_ip,
    get_list_shorted_urls,
    get_shorted_url_by_id,
    get_url_by_shortcode,
)
from urlman.web.api.urls.repos.services import (
    confirm_url_key,
    create_shorted_url,
    delete_shorted_url,
    soft_delete_shorted_url,
    update_shorted_url,
)
from urlman.web.api.urls.schemas import UrlExtended, UrlIn, UrlOut, UrlUpdate
from urlman.web.api.users.repos.selectors import get_current_user

router = APIRouter()


@router.get("/redirect/{short_code}", status_code=302)
async def redirect(
    short_code: str,
    request: Request,
    key: Optional[str] = None,
    session: AsyncSession = Depends(get_db_session),
):
    """Redirecting endpoint."""
    try:
        shorted_url = await get_url_by_shortcode(
            url_shortcode=short_code,
            session=session,
        )
        client_ip = await get_client_ip(request=request)
        await create_transition(
            client_ip=client_ip,
            url=shorted_url,
            session=session,
        )
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    if not shorted_url:
        raise UrlNotFoundException()
    if shorted_url.is_protected:
        await confirm_url_key(
            shorted_url=shorted_url,
            key=key,
            raise_exception=True,
        )
    return RedirectResponse(
        url=shorted_url.url,
        status_code=302,
    )


@router.get("/{url_id}", response_model=UrlExtended, status_code=200)
async def get_single_url(
    url_id: str,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Get single shorted url by id."""
    try:
        shorted_url = await get_shorted_url_by_id(
            url_id=url_id,
            session=session,
        )
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    if not shorted_url:
        raise UrlNotFoundException()
    return shorted_url


@router.get("", response_model=LimitOffsetPage[UrlOut], status_code=200)
async def get_list_urls(
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Get list of current users urls."""
    try:
        urls = await get_list_shorted_urls(
            user=current_user,
            session=session,
        )
    except IntegrityError as ie:
        raise HTTPException(400, detail=str(ie.orig))
    return paginate(urls)


@router.post("", response_model=UrlOut, status_code=201)
async def create_url(
    url: UrlIn,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Create shorted url."""
    try:
        shorted_url = await create_shorted_url(
            url=url,
            user=current_user,
            session=session,
        )
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return shorted_url


@router.patch("/{url_id}", response_model=UrlOut, status_code=200)
async def update_url(
    url_id: str,
    data: UrlUpdate,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Update shorted url."""
    try:
        url = await update_shorted_url(
            url_id=url_id,
            data=data,
            user=current_user,
            session=session,
        )
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return url


@router.patch("/{url_id}/soft_delete", status_code=204)
async def delete_url_soft(
    url_id: str,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Soft delete url."""
    try:
        await soft_delete_shorted_url(
            url_id=url_id,
            user=current_user,
            session=session,
        )
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))


@router.delete("/{url_id}", status_code=200)
async def delete_url_hard(
    url_id: str,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Delete url."""
    try:
        await delete_shorted_url(
            url_id=url_id,
            user=current_user,
            session=session,
        )
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))


@router.get(
    "/{url_id}/transitions",
    response_model=LimitOffsetPage[TransitionOut],
    status_code=200,
)
async def get_url_transitions(
    url_id: str,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Get all url transitions."""
    try:
        url = await get_shorted_url_by_id(
            url_id=url_id,
            session=session,
        )
        if url.user != current_user:
            raise UrlNotFoundException()
        transitions = await get_transitions_by_url(
            url=url,
            session=session,
        )
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return paginate(transitions)
