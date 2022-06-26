import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi_utils.tasks import repeat_every

from app import SETTINGS
from app.products.api import products_router

app = FastAPI(
    title=SETTINGS.APP_NAME,
    openapi_url=f"{SETTINGS.API_PREFIX}/openapi.json",
    debug=SETTINGS.DEBUG,
)
router_prefix = f"{SETTINGS.API_PREFIX}/products"

app.include_router(products_router, prefix=router_prefix, tags=["Products API"])


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")
