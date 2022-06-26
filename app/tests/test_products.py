import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.entities import Product


@pytest.mark.asyncio
async def test_create_product(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    payload = test_data["case_create"]["payload"]
    response = await async_client.post(
        "/products",
        json=payload,
    )
    assert response.status_code == 201

    got = response.json()
    expected = test_data["case_create"]["expected"]
    for k, v in expected.items():
        assert got[k] == v

    statement = select(Product).where(Product.id == got["id"])
    results = await async_session.execute(statement=statement)
    product = results.scalar_one()

    for k, v in expected.items():
        assert getattr(product, k) == v


@pytest.mark.asyncio
async def test_get_product(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    product_data = test_data["initial_data"]["product"]
    statement = insert(Product).values(product_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    response = await async_client.get(f"/products/{product_data['id']}")
    assert response.status_code == 200

    got = response.json()
    expected = test_data["case_get"]["expected"]

    for k, v in expected.items():
        assert got[k] == v


@pytest.mark.asyncio
async def test_patch_product(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    product_data = test_data["initial_data"]["product"]
    statement = insert(Product).values(product_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    payload = test_data["case_patch"]["payload"]
    response = await async_client.patch(f"/products/{product_data['id']}", json=payload)
    assert response.status_code == 200

    got = response.json()
    expected = test_data["case_patch"]["expected"]

    for k, v in expected.items():
        assert got[k] == v


@pytest.mark.asyncio
async def test_delete_product(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    product_data = test_data["initial_data"]["product"]
    statement = insert(Product).values(product_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    response = await async_client.delete(f"/products/{product_data['id']}")
    assert response.status_code == 200

    got = response.json()
    expected = test_data["case_delete"]["expected"]

    for k, v in expected.items():
        assert got[k] == v

    statement = select(Product).where(Product.id == product_data["id"])
    results = await async_session.execute(statement=statement)
    assert results.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_missing_product(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    response = await async_client.get("/products/-1")
    assert response.status_code == 404

    response = await async_client.delete("/products/-1")
    assert response.status_code == 404

    response = await async_client.patch(
        "/products/-1", json={"name": "test", "description": "patch"}
    )
    assert response.status_code == 404
