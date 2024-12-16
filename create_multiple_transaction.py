from sqlmodel import Session
from db import engine
from app.models.transactions import Transaction
from app.models.customers import Customer
session = Session(engine)
customer = Customer(
    name="Luis",
    description="Profe Platzi",
    email="hola@lcmartinez.com",
    age=33,
)
session.add(customer)
session.commit()

for x in range(100):
    session.add(
        Transaction(
            customer_id=customer.id,
            description=f"Test number {x}",
            amount=10 * x,
        )
    )
session.commit()