from fastapi import APIRouter,HTTPException,status 
from models import Customer,CustomerCreate
from db import SessionDep
from sqlmodel import select

router = APIRouter()
@router.get("/customers",response_model=list[Customer],tags=['customers'])
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@router.post("/customers", response_model=Customer,tags=['customers'])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get("/customers/{customer_id}",response_model=Customer, tags=["customers"])
async def read_customer(customer_id:int,session:SessionDep):
    customer_db= session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customer doesn't exist")
    return customer_db

@router.delete("/customers/{customer_id}", tags=["customers"])
async def delete_customer(customer_id:int,session:SessionDep):
    customer_db= session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customer doesn't exist")
    session.delete(customer_db)
    session.commit()
    return {"detail":"deleted customer"}
@router.get("/customers/{customer_id}",response_model=Customer, tags=["customers"])
async def read_customer(customer_id:int,session:SessionDep):
    customer_db= session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customer doesn't exist")
    return customer_db