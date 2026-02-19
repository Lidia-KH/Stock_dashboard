from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    sku: str
    quantity: int = 0
    min_threshold: int = 5
    price: float = 0.0

class Movement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int
    type: str
    quantity: int
    date: datetime = Field(default_factory=datetime.utcnow)