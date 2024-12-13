from pydantic import BaseModel


    
class Transaction(BaseModel):
    id:int
    amount:int
    description: str