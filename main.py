from fastapi import FastAPI
import zoneinfo
from datetime import datetime
from pydantic import BaseModel

class Customer(BaseModel):
    name:str
    description:str | None
    email:str
    age: int
app = FastAPI()


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

@app.post("/customers")
async def create_customer(customer_data:Customer):
    return customer_data