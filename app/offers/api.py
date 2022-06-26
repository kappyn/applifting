from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status

from app.core.entities import (
    Offer,
    Product,
    ProductCreate,
    ProductPatch,
    ProductRead,
    StatusMessage,
)
from app.offers import offer_service
from app.offers.crud import OfferCRUD
from app.offers.dependencies import get_offer_crud
from app.products.crud import ProductCRUD
from app.products.dependencies import get_product_crud

offers_router = APIRouter()


# @offers_router.patch(
#     "/{product_id}/offers",
#     response_model=List[Offer],
#     status_code=http_status.HTTP_200_OK,
# )
# async def update_product_offers(
#     product_id: int,
#     products: ProductCRUD = Depends(get_product_crud),
# ) -> List[Offer]:
#     await offer_service.refresh_product_offers(products)
#     return await products.get_offers(product_id)


@offers_router.get(
    "/{product_id}/offers",
    response_model=List[Offer],
    status_code=http_status.HTTP_200_OK,
)
async def get_product_offers(
    product_id: int,
    products: ProductCRUD = Depends(get_product_crud),
) -> List[Offer]:
    product = await products.get(product_id)
    return product.offers
