from fastapi import FastAPI
import zoneinfo
from datetime import datetime
from models import Customer,CustomerCreate, Transaction,Invoice
from db import SessionDep,create_all_tables
app = FastAPI(lifespan=create_all_tables)



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
@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get("/customers")
async def get_customers():
    return db_customers

@app.post("/transactions")
async def create_transaction(transaction_data:Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data:Invoice):
    return invoice_data