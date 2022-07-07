from operator import attrgetter

import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.entities import Offer, Product
from app.offers.crud import OfferCRUD
from app.products.crud import ProductCRUD


@pytest.mark.asyncio
async def test_offers_integration(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    """
    Tests offer and product integration as well as merging strategy when updates are fetched.
    A mock offer update is "fetched" from the file (on production they're fetched externally).
    """
    products_crud = ProductCRUD(session=async_session)
    offers_crud = OfferCRUD(session=async_session)

    payload = test_data["case_add_offers"]["payload"]
    product = payload["product"]

    response = await async_client.post("/products", json=product)
    assert response.status_code == 201
    product_id = response.json()["id"]

    # adding new offers for 1 currently available product
    offers = list(map(lambda offer: Offer(**offer), payload["offers"]))
    assert await products_crud.update_offers(product_id, offers)

    result_crud = sorted(await offers_crud.get_all(product_id), key=attrgetter("id"))
    expected = sorted(
        filter(lambda x: x.product_id == product_id, offers), key=attrgetter("id")
    )
    assert result_crud == expected

    # check that existing offers are overwritten correctly during update
    update = test_data["case_update_offers"]["payload"]["update"]
    offers_update = list(map(lambda offer: Offer(**offer), update))

    expected = test_data["case_update_offers"]["expected"]["offers"]
    offers_expected = sorted(
        list(map(lambda offer: Offer(**offer), expected)), key=attrgetter("id")
    )

    assert await products_crud.update_offers(product_id, offers_update)
    result_crud = sorted(await offers_crud.get_all(product_id), key=attrgetter("id"))
    assert result_crud == offers_expected


@pytest.mark.asyncio
async def test_multiple_project_update(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    """This test emulates having multiple registered products that are being updated."""
    products_crud = ProductCRUD(session=async_session)
    offers_crud = OfferCRUD(session=async_session)

    products = test_data["case_multiple_project_update"]["payload"]["products"]
    for product in products:
        statement = insert(Product).values(product)
        await async_session.execute(statement=statement)
        await async_session.commit()

    offers = test_data["case_multiple_project_update"]["payload"]["offers"]
    for offer in offers:
        statement = insert(Offer).values(offer)
        await async_session.execute(statement=statement)
        await async_session.commit()

    offer_update_data = list(
        map(
            lambda offer: Offer(**offer),
            test_data["case_multiple_project_update"]["payload"]["update"],
        )
    )
    for product in products:
        offers_update = list(
            filter(lambda offer: offer.product_id == product["id"], offer_update_data)
        )
        assert await products_crud.update_offers(product["id"], offers_update)

    results = sorted(await offers_crud.get_all(), key=attrgetter("id"))
    expected = sorted(
        list(
            map(
                lambda offer: Offer(**offer),
                test_data["case_multiple_project_update"]["expected"]["offers"],
            )
        ),
        key=attrgetter("id"),
    )

    assert results == expected
