from fastapi import APIRouter,HTTPException,status 
from ..models.customers import Customer,CustomerCreate, CustomerPlan,CustomerUpdate, Plan
from db import SessionDep
from sqlmodel import select

router = APIRouter()
@router.get("/customers",response_model=list[Customer],tags=['customers'])
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@router.get("/customers/{customer_id}",response_model=Customer, tags=["customers"])
async def read_customer(customer_id:int,session:SessionDep):
    customer_db= session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customer doesn't exist")
    return customer_db

@router.post("/customers", response_model=Customer,tags=['customers'],status_code=status.HTTP_201_CREATED)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.patch("/customers/{customer_id}",response_model=Customer, tags=["customers"],status_code=status.HTTP_201_CREATED)
async def edit_customer(customer_id:int,customer_data:CustomerUpdate,session:SessionDep):
    customer_db= session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customer doesn't exist")
    update_data = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(update_data)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db


@router.delete("/customers/{customer_id}", tags=["customers"])
async def delete_customer(customer_id:int,session:SessionDep):
    customer_db= session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customer doesn't exist")
    session.delete(customer_db)
    session.commit()
    return {"detail":"deleted customer"}
@router.post("/customers/{customer_id}/plans/{plan_id}",tags=["customers"])
async def subscribe_customer_to_plan(customer_id:int,plan_id:int,session:SessionDep):
    customer_db = session.get(Customer,customer_id)
    plan_db= session.get(Plan,plan_id)
    if not customer_db or not plan_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The customer or plan doesn't exist")
    
    customer_plan_db=CustomerPlan(plan_id=plan_db.id,customer_id=customer_db.id)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db
    
@router.get("/customers/{customer_id}/plans/",tags=["customers"])
async def get_plan_of_customer(customer_id:int, session:SessionDep):
    customer_db=session.get(Customer,customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customer not found")
    return customer_db.plans
 
    

