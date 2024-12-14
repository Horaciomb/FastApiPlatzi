from fastapi import APIRouter,HTTPException,status
from ..models.customers import Plan 
from db import SessionDep
from sqlmodel import select


router = APIRouter()

@router.get('/plans',response_model=list[Plan],tags=['plans'])
async def get_plans(session:SessionDep):
    return session.exec(select(Plan)).all() 
@router.post("/plans",response_model=Plan,tags=['plans'],status_code=status.HTTP_201_CREATED)
async def create_plan(plan_data:Plan,session: SessionDep):
   plan_db= Plan.model_validate(plan_data.model_dump())
   session.add(plan_db)
   session.commit()
   session.refresh(plan_db)
   return plan_db

    