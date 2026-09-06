from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class PortfolioHoldingBase(BaseModel):
    symbol: str
    shares: float
    average_buy_price: float

class PortfolioBase(BaseModel):
    name: str

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioResponse(PortfolioBase):
    id: int
    holdings: List[PortfolioHoldingBase] = []

    class Config:
        from_attributes = True

class AgentQuery(BaseModel):
    query: str
