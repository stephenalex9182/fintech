from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, models, auth, database
from ..agent.workflow import run_research_agent
from ..services.stock_api import get_stock_data

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
