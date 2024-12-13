from pydantic import EmailStr
from sqlmodel import SQLModel, Field

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