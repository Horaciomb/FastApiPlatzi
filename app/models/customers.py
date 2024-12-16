from typing import TYPE_CHECKING
from pydantic import EmailStr, field_validator
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Session, select
from db import engine
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
    @field_validator("name")
    @classmethod
    def validate_plan_name(cls, value):
        if not value.strip():
            raise ValueError("Plan name cannot be empty")
        
        session = Session(engine)
        query = select(Plan).where(Plan.name == value)
        result = session.exec(query).first()
        if result:
            raise ValueError("This plan name is already registered")
        return value
    
    @field_validator("price")
    @classmethod
    def validate_price(cls, value):
        if value < 0:
            raise ValueError("Price must be a positive value")
        return value

class CustomerBase(SQLModel):
    name:str=Field(default=None)
    description:str | None =Field(default=None)
    email:EmailStr = Field(default=None)
    age: int =Field(default=None)
    
    @field_validator("email")
    @classmethod
    def validate_email(cls,value):
        session= Session(engine)
        query= select(Customer).where(Customer.email==value)
        result=session.exec(query).first()
        if result:
            raise ValueError("This email address is already registered")
        return value
    
    @field_validator("age")
    @classmethod
    def validate_age(cls,value):
        if value < 18:
            raise ValueError("Customer must be at least 18 years old")
        if value > 120:
            raise ValueError("Age must be less than or equal to 120")
        return value
    
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
