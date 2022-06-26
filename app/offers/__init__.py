from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.offers.crud import OfferCRUD
from app.offers.service import OfferService

offer_service = OfferService()
