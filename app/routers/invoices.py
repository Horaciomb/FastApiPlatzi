from fastapi import APIRouter,HTTPException,status 
from ..models.invoices import Invoice
from db import SessionDep
from sqlmodel import select

router = APIRouter()

@router.post("/invoices",tags=['invoices'])
async def create_invoice(invoice_data:Invoice):
    return invoice_data