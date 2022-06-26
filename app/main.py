import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi_utils.tasks import repeat_every

from app import SETTINGS
from app.offers import offer_service
from app.offers.api import offers_router
from app.products.api import products_router

app = FastAPI(
    title=SETTINGS.APP_NAME,
    openapi_url=f"{SETTINGS.API_PREFIX}/openapi.json",
    debug=SETTINGS.DEBUG,
)
router_prefix = f"{SETTINGS.API_PREFIX}/products"

app.include_router(products_router, prefix=router_prefix, tags=["Products API"])
app.include_router(offers_router, prefix=router_prefix, tags=["Offers API"])


@repeat_every(seconds=SETTINGS.OFFERS_REFRESH_DELAY_SECONDS)
async def periodic_offer_update():
    await offer_service.refresh_product_offers()


@app.on_event("startup")
async def on_startup():
    await offer_service.get_access_token()
    await periodic_offer_update()


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")
