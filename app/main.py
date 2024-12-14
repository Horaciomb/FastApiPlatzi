from fastapi import FastAPI 
import zoneinfo
from datetime import datetime
from db import create_all_tables
from .routers.customers import router as customer_router
from .routers.transactions import router as transaction_router
from .routers.invoices import router as invoice_router
from .routers.plans import router as plan_router
app = FastAPI(lifespan=create_all_tables)

routers = [
    customer_router,
    transaction_router,
    invoice_router,
    plan_router
]
for router in routers:
    app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

country_timezones = {
    "US": "America/New_York",
    "UK": "Europe/London",
    "DE": "Europe/Berlin",
    "FR": "Europe/Paris",
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
}

@app.get("/time/{iso_code}")
async def time(iso_code:str):
    iso=iso_code.upper()
    timezone_str=country_timezones.get(iso)
    tz=zoneinfo.ZoneInfo(timezone_str)
    return {"time":datetime.now(tz)}


