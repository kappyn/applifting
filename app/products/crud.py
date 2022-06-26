from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from sqlalchemy import and_, delete, select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.entities import Offer, Product, ProductCreate, ProductPatch
from app.offers.crud import OfferCRUD


class ProductCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: ProductCreate) -> Product:
        values = data.dict()
        product = Product(**values)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get(self, product_id: int) -> Product:
        statement = (
            select(Product)
            .where(Product.id == product_id)
            .options(selectinload(Product.offers))
        )
        results = await self.session.execute(statement=statement)
        product = results.scalar_one_or_none()
        if product is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
            )
        return product

    async def get_all(self) -> List[Product]:
        statement = select(Product)
        results = await self.session.execute(statement=statement)
        products = results.scalars().all()
        if products is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
            )
        return products

    async def patch(self, product_id: int, data: ProductPatch) -> Product:
        product = await self.get(product_id=product_id)
        values = data.dict(exclude_unset=True)
        for k, v in values.items():
            setattr(product, k, v)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def _delete(self, product_id: int) -> bool:
        product = await self.get(product_id)
        await self.session.delete(product)
        await self.session.commit()
        return True
