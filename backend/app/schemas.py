from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

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

class NotificationResponse(BaseModel):
    id: int
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class AlertRuleCreate(BaseModel):
    symbol: str
    condition: str
    threshold_price: float

class AlertRuleResponse(AlertRuleCreate):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class MPTOptimizationRequest(BaseModel):
    symbols: List[str]

class MPTOptimizationResponse(BaseModel):
    optimal_weights: Dict[str, float]
    expected_return: float
    expected_volatility: float
    sharpe_ratio: float

class OptionsAnalysisResponse(BaseModel):
    symbol: str
    calls: List[Dict[str, Any]]
    puts: List[Dict[str, Any]]
    underlying_price: float

class AgentQuery(BaseModel):
    query: str
