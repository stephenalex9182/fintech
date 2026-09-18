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

class PortfolioHoldingCreate(PortfolioHoldingBase):
    pass

class FundamentalDataResponse(BaseModel):
    symbol: str
    pe_ratio: Optional[float]
    debt_to_equity: Optional[float]
    revenue_growth: Optional[float]
    profit_margins: Optional[float]
    free_cashflow: Optional[float]
    beta: Optional[float]

class MultiAssetRequest(BaseModel):
    symbols: List[str]

class RiskAnalysisResponse(BaseModel):
    portfolio_id: int
    portfolio_value: float
    total_returns: float
    volatility: float
    sharpe_ratio: float
    value_at_risk_95: float
    beta: float

class AgentQuery(BaseModel):
    query: str
