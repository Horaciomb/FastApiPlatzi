from fastapi import FastAPI 
import zoneinfo
from datetime import datetime
from models import Customer, Transaction,Invoice
from db import create_all_tables
from endpoints.customers import router as customer_router
app = FastAPI(lifespan=create_all_tables)

routers = [
    customer_router
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


db_customers:list[Customer]=[]




@app.post("/transactions" ,tags=['transactions'])
async def create_transaction(transaction_data:Transaction):
    return transaction_data

@app.post("/invoices",tags=['invoices'])
async def create_invoice(invoice_data:Invoice):
    return invoice_data