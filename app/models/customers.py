from typing import TYPE_CHECKING
from pydantic import EmailStr
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
if TYPE_CHECKING:
    from .transactions import Transaction

class StatusEnum(str, Enum):
    ACTIVE="active"
    INACTIVE="inactive"
    
class CustomerPlan(SQLModel, table=True):
    id: int = Field(primary_key=True)
    plan_id: int= Field(foreign_key="plan.id")
    customer_id: int=Field(foreign_key="customer.id")
    status:StatusEnum=Field(default=StatusEnum.ACTIVE)
    
class Plan(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str = Field(default=None)
    price: int = Field(default=None)
    descripcion: str = Field(default=None)
    customers: list["Customer"] = Relationship(
        back_populates="plans", link_model=CustomerPlan
    )

class CustomerBase(SQLModel):
    name:str=Field(default=None)
    description:str | None =Field(default=None)
    email:EmailStr = Field(default=None)
    age: int =Field(default=None)
    
class CustomerCreate(CustomerBase):
    pass
class CustomerUpdate(CustomerBase):
    pass


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"]= Relationship(back_populates="customer")
    plans: list[Plan] = Relationship(
        back_populates="customers", link_model=CustomerPlan
    )
