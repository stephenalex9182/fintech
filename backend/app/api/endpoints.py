from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, models, auth, database
from ..agent.workflow import run_research_agent
from ..services.stock_api import get_stock_data
from ..services.fundamental_analysis import get_fundamental_data
from ..services.multi_asset_analysis import analyze_multiple_assets
from ..services.risk_analysis import calculate_portfolio_risk
from ..services.mpt_optimization import optimize_portfolio
from ..services.market_alerts import evaluate_market_alerts
from ..services.derivatives_analysis import get_options_data
router = APIRouter()

@router.post("/research")
def perform_research(query: schemas.AgentQuery, current_user: models.User = Depends(auth.get_current_user)):
    """Run LangGraph AI Agent on user query"""
    result = run_research_agent(query.query)
    return {"query": query.query, "result": result}

@router.get("/stock/{symbol}")
def get_stock_info(symbol: str, current_user: models.User = Depends(auth.get_current_user)):
    """Fetch cached stock data"""
    data = get_stock_data(symbol)
    return data

@router.get("/fundamentals/{symbol}", response_model=schemas.FundamentalDataResponse)
def get_fundamentals(symbol: str, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Fetch fundamental data for a stock"""
    return get_fundamental_data(symbol, db)

@router.post("/analysis/multi-asset")
def multi_asset_analysis(request: schemas.MultiAssetRequest, current_user: models.User = Depends(auth.get_current_user)):
    """Analyze multiple assets for correlation and comparative performance"""
    return analyze_multiple_assets(request.symbols)

@router.post("/portfolio", response_model=schemas.PortfolioResponse)
def create_portfolio(portfolio: schemas.PortfolioCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Create a new portfolio for user"""
    new_portfolio = models.Portfolio(name=portfolio.name, owner=current_user)
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)
    return new_portfolio

@router.get("/portfolio", response_model=list[schemas.PortfolioResponse])
def get_portfolios(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Get all portfolios for current user"""
    return db.query(models.Portfolio).filter(models.Portfolio.user_id == current_user.id).all()

@router.get("/portfolio/{portfolio_id}", response_model=schemas.PortfolioResponse)
def get_portfolio(portfolio_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Get a specific portfolio"""
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id, models.Portfolio.user_id == current_user.id).first()
    if not portfolio:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

@router.post("/portfolio/{portfolio_id}/holdings", response_model=schemas.PortfolioResponse)
def add_portfolio_holding(portfolio_id: int, holding: schemas.PortfolioHoldingCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Add a holding to a portfolio"""
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id, models.Portfolio.user_id == current_user.id).first()
    if not portfolio:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Check if holding already exists, if so update it, else create
    existing_holding = db.query(models.PortfolioHolding).filter(models.PortfolioHolding.portfolio_id == portfolio_id, models.PortfolioHolding.symbol == holding.symbol).first()
    if existing_holding:
        existing_holding.shares += holding.shares
        # basic avg price calc
        existing_holding.average_buy_price = ((existing_holding.shares - holding.shares) * existing_holding.average_buy_price + holding.shares * holding.average_buy_price) / existing_holding.shares
    else:
        new_holding = models.PortfolioHolding(
            portfolio_id=portfolio_id,
            symbol=holding.symbol,
            shares=holding.shares,
            average_buy_price=holding.average_buy_price
        )
        db.add(new_holding)
    db.commit()
    db.refresh(portfolio)
    return portfolio

@router.delete("/portfolio/{portfolio_id}/holdings/{symbol}")
def delete_portfolio_holding(portfolio_id: int, symbol: str, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Remove a holding from a portfolio"""
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id, models.Portfolio.user_id == current_user.id).first()
    if not portfolio:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Portfolio not found")
        
    holding = db.query(models.PortfolioHolding).filter(models.PortfolioHolding.portfolio_id == portfolio_id, models.PortfolioHolding.symbol == symbol).first()
    if not holding:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Holding not found")
        
    db.delete(holding)
    db.commit()
    return {"message": "Holding deleted successfully"}

@router.get("/portfolio/{portfolio_id}/risk", response_model=schemas.RiskAnalysisResponse)
def get_portfolio_risk(portfolio_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Calculate portfolio risk metrics"""
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id, models.Portfolio.user_id == current_user.id).first()
    if not portfolio:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Portfolio not found")
        
    risk_metrics = calculate_portfolio_risk(portfolio_id, db)
    if not risk_metrics:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Could not calculate risk metrics. Does the portfolio have holdings?")
        
    return risk_metrics

@router.post("/portfolio/optimize", response_model=schemas.MPTOptimizationResponse)
def optimize_mpt(request: schemas.MPTOptimizationRequest, current_user: models.User = Depends(auth.get_current_user)):
    """Optimize portfolio using Modern Portfolio Theory"""
    result = optimize_portfolio(request.symbols)
    if "error" in result:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/alerts", response_model=schemas.AlertRuleResponse)
def create_alert_rule(rule: schemas.AlertRuleCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Create a new market alert rule"""
    new_rule = models.AlertRule(
        user_id=current_user.id,
        symbol=rule.symbol,
        condition=rule.condition,
        threshold_price=rule.threshold_price
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule

@router.get("/alerts", response_model=list[schemas.AlertRuleResponse])
def get_alerts(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Get all alert rules for current user"""
    return db.query(models.AlertRule).filter(models.AlertRule.user_id == current_user.id).all()

@router.post("/alerts/evaluate")
def evaluate_alerts(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Manually trigger alert evaluation"""
    return evaluate_market_alerts(db)

@router.get("/notifications", response_model=list[schemas.NotificationResponse])
def get_notifications(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Get user notifications"""
    return db.query(models.Notification).filter(models.Notification.user_id == current_user.id).order_by(models.Notification.created_at.desc()).all()

@router.put("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Mark notification as read"""
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id, models.Notification.user_id == current_user.id).first()
    if not notification:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.is_read = True
    db.commit()
    return {"message": "Notification marked as read"}

@router.get("/options/{symbol}", response_model=schemas.OptionsAnalysisResponse)
def get_options(symbol: str, current_user: models.User = Depends(auth.get_current_user)):
    """Get options chain analysis for a symbol"""
    result = get_options_data(symbol)
    if "error" in result:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=result["error"])
    return result
