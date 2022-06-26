from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.offers.crud import OfferCRUD


async def get_offer_crud(
    session: AsyncSession = Depends(get_async_session),
) -> OfferCRUD:
    return OfferCRUD(session=session)
