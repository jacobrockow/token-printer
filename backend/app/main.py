from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes_preview import router as preview_router
from app.api.routes_search import router as search_router
from app.api.routes_print import router as print_router
from app.api.routes_mobile import router as mobile_router
from app.api.routes_momir import router as momir_router

app = FastAPI(title="Token Printer API")

app.include_router(search_router)
app.include_router(preview_router)
app.include_router(print_router)
app.include_router(mobile_router)
app.include_router(momir_router)

app.mount("/generated", StaticFiles(directory="app/generated"), name="generated")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
