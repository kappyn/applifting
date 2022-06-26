from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.entities import Offer, Product


class OfferCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: Offer) -> Offer:
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def get(self, offer_id: int) -> Optional[Offer]:
        statement = select(Offer).where(Offer.id == offer_id)
        results = await self.session.execute(statement=statement)
        return results.scalar_one_or_none()

    async def get_all(
        self,
        product_id: Optional[int] = None,
    ) -> List[Offer]:
        statement = select(Offer)
        if product_id is not None:
            statement = select(Offer).where(Offer.product_id == product_id)
        results = await self.session.execute(statement=statement)
        return results.scalars().all()

    async def patch(self, offer_id: int, data: Offer) -> bool:
        offer = await self.get(offer_id=offer_id)
        if offer is None:
            return False
        values = data.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(offer, k, v)
        self.session.add(offer)
        await self.session.commit()
        await self.session.refresh(offer)
        return True

    # async def _delete(self, offer: Offer) -> bool:
    #     await self.session.delete(offer)
    #     await self.session.commit()
    #     return True
