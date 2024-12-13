from fastapi import FastAPI,HTTPException,status 
import zoneinfo
from datetime import datetime
from models import Customer,CustomerCreate, Transaction,Invoice
from db import SessionDep,create_all_tables
from sqlmodel import select
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
@app.post("/customers", response_model=Customer,tags=['customers'])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get("/customers",response_model=list[Customer],tags=['customers'])
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@app.get("/customers/{customer_id}", tags=['customers'])   
async def get_customer(customer_id: int, session: SessionDep):
    if  session.get(Customer, customer_id) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return session.get(Customer, customer_id)

@app.post("/transactions" ,tags=['transactions'])
async def create_transaction(transaction_data:Transaction):
    return transaction_data

@app.post("/invoices",tags=['invoices'])
async def create_invoice(invoice_data:Invoice):
    return invoice_data