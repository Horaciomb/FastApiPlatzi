from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .customers import Customer
class TransactionBase(SQLModel):
    amount:int =Field(default=None)
    description: str =Field(default=None)
  
class TransactionCreate(TransactionBase):
    customer_id: int = Field(foreign_key="customer.id")
class TransactionUpdate(TransactionBase):
    customer_id: int = Field(foreign_key="customer.id")  
    
class Transaction(TransactionBase, table=True):
    id:int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Optional["Customer"] = Relationship(back_populates="transactions")
