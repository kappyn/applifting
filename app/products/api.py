from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status

from app import SETTINGS
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

products_router = APIRouter()


@products_router.post(
    "", response_model=ProductRead, status_code=http_status.HTTP_201_CREATED
)
async def create_product(
    data: ProductCreate, products: ProductCRUD = Depends(get_product_crud)
):
    product = await products.create(data=data)
    await offer_service.register_product(product)
    return product


@products_router.get(
    "", response_model=List[ProductRead], status_code=http_status.HTTP_200_OK
)
async def get_products(products: ProductCRUD = Depends(get_product_crud)):
    return await products.get_all()


@products_router.get(
    "/{product_id}",
    response_model=ProductRead,
    status_code=http_status.HTTP_200_OK,
)
async def get_product_by_id(
    product_id: int, products: ProductCRUD = Depends(get_product_crud)
):
    return await products.get(product_id=product_id)


@products_router.patch(
    "/{product_id}", response_model=ProductRead, status_code=http_status.HTTP_200_OK
)
async def patch_product_by_id(
    product_id: int,
    data: ProductPatch,
    products: ProductCRUD = Depends(get_product_crud),
):
    return await products.patch(product_id=product_id, data=data)


@products_router.delete(
    "/{product_id}", response_model=StatusMessage, status_code=http_status.HTTP_200_OK
)
async def delete_product_by_id(
    product_id: int, products: ProductCRUD = Depends(get_product_crud)
):
    await products._delete(product_id=product_id)
    return {"message": "Product deleted successfully."}
