from pydantic import BaseModel
from .customers import Customer
from .transactions import Transaction

class Invoice(BaseModel):
    id:int
    customer: Customer
    transactions: list[Transaction]
    total: int
    @property
    def amount_total(self):
        return sum(transaction.amount for transaction in self.transactions)
    def __init__(self, **data):
        super().__init__(**data)
        self.total = self.ammount_total
    