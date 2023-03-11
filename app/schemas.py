from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# schema para producto

class Product(BaseModel):
  id: Optional[int]
  name: str
  price: int
  qty: int
  is_active: Optional[bool]
  category_id: int
  created_at: Optional[datetime]
  
  class Config:
    orm_mode = True
    
# schema para categoria

class Category(BaseModel):
  id: Optional[int]
  name: str
  is_active: Optional[bool]
  created_at: Optional[datetime]
  
  class Config:
    orm_mode = True    

