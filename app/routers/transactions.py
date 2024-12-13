from fastapi import APIRouter,HTTPException,status 
from ..models.transactions import Transaction
from db import SessionDep
from sqlmodel import select

router = APIRouter()
@router.post("/transactions" ,tags=['transactions'])
async def create_transaction(transaction_data:Transaction):
    return transaction_data