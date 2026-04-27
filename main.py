from fastapi import FastAPI

from app.routers import construction, health, markets, opex

app = FastAPI(title="Enigma BE", version="0.1.0")

app.include_router(health.router)
app.include_router(markets.router)
app.include_router(opex.router)
app.include_router(construction.router)
