from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.products.crud import ProductCRUD


async def get_product_crud(
    session: AsyncSession = Depends(get_async_session),
) -> ProductCRUD:
    return ProductCRUD(session=session)
