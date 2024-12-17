from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request ,status
import time
import zoneinfo
from datetime import datetime
from fastapi.security import  HTTPBasic, HTTPBasicCredentials
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
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time=time.time()
    response =await call_next(request)
    procces_time=time.time() - start_time
    print(f"Request: {request.url} completed in: {procces_time:.4f} seconds")
    return response
# @app.middleware("http") 
# async def log_request_headers(request: Request, call_next):
    
#     print("Request Headers:")
#     for header, value in request.headers.items():
#         print(f"{header}: {value}")

#     response = await call_next(request) 

#     return response
security=HTTPBasic()
@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials,Depends(security)]):
    print(credentials)
    if credentials.username == "horacio" and credentials.password=="1234":
        return {"message": f"Hello, {credentials.username}"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

country_timezones = {
    "US": "America/New_York",
    "UK": "Europe/London",
    "DE": "Europe/Berlin",
    "FR": "Europe/Paris",
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
}

@app.get("/time/{iso_code}")
async def get_time_by_isocode(iso_code:str):
    iso=iso_code.upper()
    timezone_str=country_timezones.get(iso)
    tz=zoneinfo.ZoneInfo(timezone_str)
    return {"time":datetime.now(tz)}


