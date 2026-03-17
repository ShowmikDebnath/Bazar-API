from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime




'''
# Users Schemas
'''

# What data is needed to create a user
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# What data to show when returning a user
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True



'''
# Product Schemas
'''

# What data is needed to create a product
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    category: Optional[str] = None


# What data to show when returning a product
class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    quantity: int
    category: Optional[str]

    class Config:
        from_attributes = True



'''
# Cart Schemas
'''

# What data is needed to create a Cart
class CartCreate(BaseModel):
    product_id: int
    quantity: int


# What data to show when returning a Cart
class CartResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


'''
# Order Schemas
'''


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True




class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime
    order_items: List[OrderItemResponse] = []
    

    class Config:
        from_attributes = True



'''
# Auth Schemas
'''

class Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


