from fastapi import APIRouter,HTTPException,status 
from ..models.transactions import Transaction,TransactionCreate,TransactionUpdate
from ..models.customers import Customer
from db import SessionDep
from sqlmodel import select

router = APIRouter()
@router.get("/transactions",response_model=list[Transaction] ,tags=['transactions'])
async def get_transactions(session:SessionDep):
    return session.exec(select(Transaction)).all() 

@router.get("/transactions/{transaction_id}", response_model=Transaction, tags=["transactions"])
async def read_transaction(transaction_id: int, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction doesn't exist"
        )
    return transaction_db

@router.post("/transactions", response_model=Transaction, tags=["transactions"], status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction_data_dict=transaction_data.model_dump()
    customer= session.get(Customer, transaction_data_dict.get('customer_id'))
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer not found')
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

@router.patch("/transactions/{transaction_id}", response_model=Transaction, tags=["transactions"], status_code=status.HTTP_200_OK)
async def edit_transaction(transaction_id: int, transaction_data: TransactionUpdate, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction doesn't exist"
        )
    update_data = transaction_data.model_dump(exclude_unset=True)
    transaction_db.sqlmodel_update(update_data)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

@router.delete("/transactions/{transaction_id}", tags=["transactions"])
async def delete_transaction(transaction_id: int, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction doesn't exist"
        )
    session.delete(transaction_db)
    session.commit()
    return {"detail": "Deleted transaction"}