from functools import lru_cache
from typing import Dict, List

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from sqlalchemy.ext.asyncio import AsyncSession

from app import SETTINGS
from app.core.db import get_async_session_cm
from app.core.entities import Offer, Product, ProductCreate, StatusMessage
from app.offers.crud import OfferCRUD
from app.offers.dependencies import get_offer_crud
from app.products.crud import ProductCRUD
from app.products.dependencies import get_product_crud


@lru_cache(maxsize=1)
class OfferService:
    def __init__(self, api_url: str = SETTINGS.OFFERS_MS_URL) -> None:
        self.client = httpx.AsyncClient(base_url=api_url)
        self.api_url = api_url
        self.access_token = None
        self.session = None

    def get_auth_headers(self) -> Dict:
        return {"Bearer": self.access_token}

    async def get_access_token(self) -> bool:
        response = await self.client.post("/auth")
        if response.status_code != 201:
            return False
        data = response.json()
        self.access_token = data["access_token"]
        print(f"access-token received: {self.access_token}")
        return True

    async def register_product(self, product: Product) -> StatusMessage:
        if self.access_token is None:
            return StatusMessage(message="API access_token isn't loaded.")
        response = await self.client.post(
            "/products/register", data=product.json(), headers=self.get_auth_headers()
        )
        if response.status_code == 400:
            raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST)
        elif response.status_code == 401:
            raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED)
        elif response.status_code != 201:
            raise HTTPException(status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE)
        return StatusMessage(message="Product registered successfully.")

    async def fetch_product_offers(self, product_id: int) -> List[Offer]:
        response = await self.client.get(
            f"/products/{product_id}/offers", headers=self.get_auth_headers()
        )
        if response.status_code == 400:
            raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST)
        elif response.status_code == 401:
            raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED)
        elif response.status_code == 404:
            raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND)
        elif response.status_code != 200:
            raise HTTPException(status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE)
        return list(map(lambda offer: Offer(**offer), response.json()))

    async def refresh_product_offers(self) -> bool:
        async with get_async_session_cm() as session:
            products_crud = ProductCRUD(session)
            products_list = await products_crud.get_all()
            print(products_list)
            for product in products_list:
                offers = await self.fetch_product_offers(product.id)
                await products_crud.update_offers(product.id, offers)
        print("Offers refreshed.")
        return True
