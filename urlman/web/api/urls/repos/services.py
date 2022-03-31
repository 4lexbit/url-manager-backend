from typing import Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from urlman.db.models.urls import UrlModel
from urlman.db.models.user import UserModel
from urlman.services.generators import generate_shortcode
from urlman.web.api.urls.exceptions import UrlKeyMatchingException, UrlNotFoundException
from urlman.web.api.urls.repos.selectors import get_shorted_url_by_id
from urlman.web.api.urls.schemas import UrlIn, UrlUpdate


async def create_shorted_url(
    *,
    url: UrlIn,
    user: UserModel,
    session: AsyncSession,
) -> Optional[UrlModel]:
    """Create new shorted url."""
    if not url.short_code:
        url.short_code = await generate_shortcode()
    if url.is_protected and not url.key:
        raise HTTPException(
            status_code=400,
            detail="Protected url must have a key",
        )
    shorted_url = UrlModel(
        url=url.url,
        short_code=url.short_code,
        is_protected=url.is_protected,
        key=url.key,
        user=user,
        user_id=user.id,
    )
    session.add(shorted_url)
    await session.commit()
    await session.refresh(shorted_url)
    return shorted_url


async def update_shorted_url(
    *,
    url_id: str,
    data: UrlUpdate,
    user: UserModel,
    session: AsyncSession,
) -> Optional[UrlModel]:
    """Update shorted url."""
    url = await get_shorted_url_by_id(url_id=url_id, session=session)
    if (url is None) or (url.user != user):
        raise UrlNotFoundException()

    updated_data = data.dict(exclude_none=True, exclude_unset=True)
    url_data = jsonable_encoder(
        url,
        exclude_none=True,
        exclude_unset=True,
    )

    for field in url_data:
        if field in updated_data:
            setattr(url, field, updated_data.get(field))

    if url.is_protected and not url.key:
        raise UrlKeyMatchingException()

    await session.commit()
    await session.refresh(url)
    return url


async def delete_shorted_url(
    *,
    url_id: str,
    user: UserModel,
    session: AsyncSession,
) -> None:
    """Delete shorted url from db."""
    url = await get_shorted_url_by_id(
        url_id=url_id,
        session=session,
    )
    if (url is None) or (url.user != user):
        raise UrlNotFoundException()
    await session.delete(url)
    await session.commit()


async def soft_delete_shorted_url(
    *,
    url_id: str,
    user: UserModel,
    session: AsyncSession,
) -> Optional[UrlModel]:
    """Change is_deleted to True."""
    url = await get_shorted_url_by_id(
        session=session,
        url_id=url_id,
    )

    if (url is None) or (url.user != user) or url.is_deleted:
        raise UrlNotFoundException()

    url.is_deleted = True
    url.deleted_at = func.now()
    await session.commit()
    return url


async def confirm_url_key(
    *,
    shorted_url: UrlModel,
    key: Optional[str],
    raise_exception: bool = True,
) -> bool:
    """Compare url keys."""
    if key:
        if shorted_url.key == key:
            return True
    if raise_exception:
        raise UrlKeyMatchingException()

    return False
